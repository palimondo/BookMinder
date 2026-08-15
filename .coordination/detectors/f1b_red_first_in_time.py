#!/usr/bin/env python3
"""F1b red-first-in-time: transcript-timeline TDD process-fidelity detector.

Reads a Claude-Code-native session transcript (JSONL) and reports, one line
per finding, timeline violations of red-first discipline: implementation
edits with no prior observed failing spec run, claimed-RED never actually
run, first-run-PASS on a new spec treated as done, RED never committed
before implementation, GREEN built upon before being committed, story-card
changes not committed before code, and commit messages implying a red state
the transcript timeline contradicts (retro-staged-grammar).

Exit 0 = clean, 1 = findings.
"""

import argparse
import json
import re
import sys
from pathlib import PurePosixPath

EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
EXCLUDED_DIRS = (
    ".coordination/",
    ".claude/",
    "docs/",
    "scratchpad/",
    "claude-dev-log-diary/",
)
LOOKAHEAD = 20

CLAIM_RED_RE = re.compile(
    r"(fail(?:s|ed|ing)? as expected"
    r"|confirm(?:ed)?\s+(?:the\s+)?(?:spec|test)s?\s+fail"
    r"|watch(?:ed)?\s+(?:it|the\s+(?:spec|test))\s+fail"
    r"|\bRED\b\s+(?:phase\s+)?(?:confirmed|verified|observed|achieved)"
    r"|(?:confirmed|verified|observed)\s+(?:the\s+)?RED\b"
    r"|\b(?:spec|test)\s+(?:is\s+|now\s+)?failing\b"
    r"|\b(?:spec|test)\s+fails\b)",
    re.IGNORECASE,
)
INVESTIGATE_RE = re.compile(
    r"(should (?:have )?fail"
    r"|never (?:been |was )?red"
    r"|why (?:did|does) (?:it|this|the (?:spec|test)) pass"
    r"|defect in the spec"
    r"|suspicious"
    r"|tautolog"
    r"|prove (?:it|the assertion) can fail"
    r"|T-12)",
    re.IGNORECASE,
)
RED_MSG_RE = re.compile(
    r"((^|\W)RED:(\s|$)|\bfailing (spec|test)s?\b)", re.IGNORECASE
)


def is_spec(path: str) -> bool:
    p = path.lstrip("./")
    name = PurePosixPath(p).name
    if not name.endswith(".py"):
        return False
    return (
        name.endswith("_spec.py")
        or name.startswith("test_")
        or "/specs/" in f"/{p}"
        or "/tests/" in f"/{p}"
    )


def is_story(path: str) -> bool:
    p = path.lstrip("./")
    return bool(re.search(r"(^|/)stories/.+\.ya?ml$", p))


def is_impl(path: str) -> bool:
    p = path.lstrip("./")
    name = PurePosixPath(p).name
    if not name.endswith(".py") or name == "conftest.py" or is_spec(p):
        return False
    rel = re.sub(r"^/home/[^/]+/[^/]+/", "", p)
    return not any(f"/{d}" in f"/{rel}" for d in EXCLUDED_DIRS)


def result_text(block: dict) -> str:
    c = block.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return "\n".join(
            b.get("text", "") for b in c if isinstance(b, dict)
        )
    return ""


def pytest_command(cmd: str):
    """Return list of .py targets if cmd runs pytest in command position, else None."""
    for seg in re.split(r"[;&|]+", cmd):
        toks = seg.strip().split()
        while toks and re.match(r"^\w+=", toks[0]):
            toks = toks[1:]
        if not toks:
            continue
        head = PurePosixPath(toks[0]).name
        rest = toks[1:]
        run = False
        if head == "pytest":
            run = True
        elif head in ("python", "python3") and len(rest) >= 2 and rest[0] == "-m" and rest[1] == "pytest":
            run, rest = True, rest[2:]
        elif head == "uv" and len(rest) >= 2 and rest[0] == "run" and rest[1] == "pytest":
            run, rest = True, rest[2:]
        if run:
            return [t.split("::")[0] for t in rest if ".py" in t and not t.startswith("-")]
    return None


def bash_written_paths(cmd: str):
    return re.findall(r"(?:>>?|\btee\s+(?:-a\s+)?)\s*([^\s;|&'\"]+\.py)\b", cmd)


def commit_messages(cmd: str):
    msgs = []
    for m in re.finditer(r"-m\s+(?:'([^']*)'|\"([^\"]*)\"|(\S+))", cmd):
        msgs.append(next(g for g in m.groups() if g is not None))
    return " ".join(msgs)


def parse_events(path: str):
    """Yield normalized events in transcript order.

    kinds: edit(path,cls), run(targets,failed,passed), commit(msg,cmd), text(text)
    Edits and runs register at tool_result time (only successful edits count).
    """
    pending = {}
    events = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = e.get("timestamp", "")
            etype = e.get("type")
            content = e.get("message", {}).get("content") if etype in ("assistant", "user") else None
            if not isinstance(content, list):
                continue
            for b in content:
                if not isinstance(b, dict):
                    continue
                if etype == "assistant" and b.get("type") == "text":
                    events.append({"kind": "text", "line": lineno, "ts": ts, "text": b.get("text", "")})
                elif etype == "assistant" and b.get("type") == "tool_use":
                    pending[b.get("id")] = {"name": b.get("name"), "input": b.get("input") or {}, "line": lineno, "ts": ts}
                elif etype == "user" and b.get("type") == "tool_result":
                    use = pending.pop(b.get("tool_use_id"), None)
                    if not use:
                        continue
                    name, inp = use["name"], use["input"]
                    loc = {"line": lineno, "ts": ts, "use_line": use["line"]}
                    if name in EDIT_TOOLS and not b.get("is_error"):
                        p = inp.get("file_path") or inp.get("notebook_path") or ""
                        events.append({"kind": "edit", "path": p, **loc})
                    elif name == "Bash":
                        cmd = inp.get("command", "")
                        out = result_text(b)
                        targets = pytest_command(cmd)
                        if targets is not None:
                            failed = bool(b.get("is_error")) or bool(
                                re.search(
                                    r"\b\d+ failed\b|\b\d+ errors?\b|\bFAILED\b|\bERROR\b"
                                    r"|ModuleNotFoundError|ImportError|Traceback",
                                    out,
                                )
                            )
                            passed = (not failed) and bool(re.search(r"\b\d+ passed\b", out))
                            events.append({"kind": "run", "targets": targets, "failed": failed, "passed": passed, **loc})
                        if re.search(r"\bgit\b[^;|&]*\bcommit\b", cmd) and not b.get("is_error"):
                            events.append({"kind": "commit", "msg": commit_messages(cmd), "cmd": cmd, **loc})
                        for wp in bash_written_paths(cmd):
                            if not b.get("is_error"):
                                events.append({"kind": "edit", "path": wp, **loc})
    return events


def classify_edit(path: str):
    if is_story(path):
        return "story"
    if is_spec(path):
        return "spec"
    if is_impl(path):
        return "impl"
    return None


def run_covers(targets, spec_path):
    if not targets:
        return True
    base = PurePosixPath(spec_path).name
    return any(PurePosixPath(t).name == base for t in targets)


def detect(events):
    findings = []

    def flag(mode, rule, ev, detail):
        findings.append(
            f"{mode} [{rule}] line={ev['line']} ts={ev.get('ts', '')}: {detail}"
        )

    spec_edited = []  # paths in order
    earned_red = False  # some spec edit followed by an observed failing run
    any_fail_run = False
    last_run = None  # 'fail' | 'pass'
    red_open = False
    red_commit_seen = False
    red_missing_flagged = False
    green_pending = False
    green_flagged = False
    story_uncommitted = None
    first_run = {}  # spec path -> (event index, passed)

    for i, ev in enumerate(events):
        k = ev["kind"]
        if k == "edit":
            cls = classify_edit(ev["path"])
            if cls == "story":
                if story_uncommitted is None:
                    story_uncommitted = ev
            elif cls in ("spec", "impl"):
                if story_uncommitted is not None:
                    flag(
                        "story-edit-before-story-commit",
                        "T-33",
                        ev,
                        f"{ev['path']} edited while story card {story_uncommitted['path']} "
                        f"(line={story_uncommitted['line']}) is uncommitted",
                    )
                    story_uncommitted = None
                if green_pending and not green_flagged:
                    flag(
                        "green-not-committed",
                        "T-17",
                        ev,
                        f"{ev['path']} edited before committing the observed GREEN",
                    )
                    green_flagged = True
                if cls == "spec":
                    if ev["path"] not in spec_edited:
                        spec_edited.append(ev["path"])
                else:
                    if not earned_red:
                        flag(
                            "edit-before-red",
                            "T-10",
                            ev,
                            f"implementation edit to {ev['path']} with no observed "
                            "failing spec run earlier in transcript",
                        )
                    if red_open and not red_commit_seen and not red_missing_flagged:
                        flag(
                            "red-commit-missing",
                            "T-14",
                            ev,
                            f"implementation edit to {ev['path']} after observed RED "
                            "with no RED commit in between",
                        )
                        red_missing_flagged = True
        elif k == "run":
            for s in spec_edited:
                if s not in first_run and run_covers(ev["targets"], s):
                    first_run[s] = (i, ev["passed"])
            if ev["failed"]:
                any_fail_run = True
                if spec_edited and (
                    not ev["targets"]
                    or any(run_covers(ev["targets"], s) for s in spec_edited)
                ):
                    earned_red = True
                if not red_open:
                    red_open = True
                    red_commit_seen = False
                    red_missing_flagged = False
                last_run = "fail"
            elif ev["passed"]:
                if red_open:
                    red_open = False
                    green_pending = True
                    green_flagged = False
                last_run = "pass"
        elif k == "text":
            if CLAIM_RED_RE.search(ev["text"]) and not any_fail_run:
                snippet = CLAIM_RED_RE.search(ev["text"]).group(0)
                flag(
                    "claimed-red-never-run",
                    "T-10",
                    ev,
                    f'assistant claims a red state ("{snippet}") with no failing '
                    "pytest run observed anywhere earlier",
                )
        elif k == "commit":
            if red_open:
                red_commit_seen = True
            green_pending = False
            green_flagged = False
            story_uncommitted = None
            if RED_MSG_RE.search(ev["msg"] or "") and last_run != "fail":
                flag(
                    "retro-staged-grammar",
                    "T-14",
                    ev,
                    f'commit message implies red state ("{ev["msg"]}") but the '
                    f"latest observed pytest run was {last_run or 'absent'}",
                )
            toks = re.findall(r"[\w./-]+", ev["cmd"])
            has_story = any(is_story(t) for t in toks)
            has_code = any(is_spec(t) or is_impl(t) for t in toks)
            if has_story and has_code:
                flag(
                    "story-card-mixed-with-code",
                    "T-33",
                    ev,
                    "git add/commit stages story-card and spec/impl files together",
                )

    for s, (i, passed) in first_run.items():
        if not passed:
            continue
        window = events[i + 1 : i + 1 + LOOKAHEAD]
        investigated = any(
            (w["kind"] == "text" and INVESTIGATE_RE.search(w["text"]))
            or (w["kind"] == "edit" and w["path"] == s)
            for w in window
        )
        if not investigated:
            flag(
                "first-run-pass-treated-as-done",
                "T-12",
                events[i],
                f"first observed run of new spec {s} passed and no "
                "investigation followed",
            )

    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--transcript", required=True, help="Claude Code session JSONL")
    args = ap.parse_args()
    events = parse_events(args.transcript)
    findings = detect(events)
    for f in findings:
        print(f)
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
