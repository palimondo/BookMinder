"""Schema gate for mining YAMLs. Usage: validate_mining.py <yaml>... Exit 1 on any violation."""

import re
import sys
from pathlib import Path

import yaml

DIARY = Path("/home/user/BookMinder/claude-dev-log-diary")
SHARDS = Path(__file__).parent / "v2" / "shards"

ENUMS = {
    "source": {"user-verbatim", "user-paraphrase", "agent-synthesis"},
    "because_source": {"user-verbatim", "user-paraphrase", "agent-synthesis"},
    "taught_or_enforced": {"taught-once", "repeated", "needed-enforcement"},
    "skill_target": {"tdd-bdd", "project-memory", "pair-programming", "claude-md"},
    "era_class": {"timeless-discipline", "2025-agentic", "harness-solved", "model-artifact"},
    "detectable_by": {"git", "transcript", "both"},
}
REQUIRED = {
    "philosophy": ["statement", "source", "loc", "feeds"],
    "skill_rules": ["rule_id", "rule", "because", "because_source", "evidence",
                    "taught_or_enforced", "skill_target", "overlap", "feasibility"],
    "failure_modes": ["name", "era_class", "detector_family", "loc", "quote",
                      "what_happened", "user_intervention", "outcome",
                      "detectable_by", "detector_candidate", "rule_origin"],
    "pairing_gems": ["loc", "why_exemplary"],
}
LOC_RE = re.compile(r"^day-\d{3}(-s\d)?:L\d+")


GLYPHS = "│╭╮╰╯─┃|✦⏺⎿»✻"


def norm(s: str) -> str:
    t = "".join(str(s).split())
    return t.translate({ord(c): None for c in GLYPHS})


def norm_source(text: str) -> str:
    # shard files prefix each line with "NNNN\t" — strip before normalizing
    return norm(re.sub(r"^\d+\t", "", text, flags=re.M))


def source_text(day: str) -> str:
    for base in (DIARY / f"{day}.md", SHARDS / f"{day}.md"):
        if base.exists():
            return norm_source(base.read_text(errors="replace"))
    return ""


def check(path: Path) -> list[str]:
    errs = []
    try:
        doc = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        return [f"unparseable YAML: {e}"]
    for top in ("file", "date", "agent_era"):
        if not doc.get(top):
            errs.append(f"missing top-level field: {top}")
    day = str(doc.get("file", ""))
    body = source_text(day.split(":")[0]) or source_text(day.replace("day-020-", "day-020-"))
    if day.startswith("day-020-"):
        body = body or source_text(day)
    if not body:
        base = day.split("-s")[0] if "-s" in day else day
        body = source_text(base)
    for section, fields in REQUIRED.items():
        for i, item in enumerate(doc.get(section) or []):
            where = f"{section}[{i}]"
            for f in fields:
                if item.get(f) in (None, ""):
                    errs.append(f"{where}: missing {f}")
            for f, allowed in ENUMS.items():
                if f in item and item[f] not in allowed and not str(item.get(f, "")).startswith("needs-rework"):
                    if f != "feasibility":
                        errs.append(f"{where}: bad enum {f}={item[f]!r}")
            loc = item.get("loc") or item.get("evidence") or ""
            if loc and not LOC_RE.match(str(loc)):
                errs.append(f"{where}: malformed loc {loc!r}")
            if item.get("source") == "user-verbatim" or item.get("because_source") == "user-verbatim":
                if not item.get("quote"):
                    errs.append(f"{where}: user-verbatim without quote")
            q = item.get("quote")
            if q and body:
                if len(str(q).splitlines()) > 3:
                    errs.append(f"{where}: quote exceeds 3 lines")
                frags = [norm(f) for f in re.split(r"\.\.\.|…|\n", str(q)) if norm(f)]
                pos = 0
                ok = True
                for frag in frags:
                    i = body.find(frag[:120], pos)
                    if i < 0:
                        ok = False
                        break
                    pos = i + 1
                if not ok:
                    errs.append(f"{where}: quote NOT verbatim in source ({str(q)[:50]!r}...)")
    return errs


fail = False
for arg in sys.argv[1:]:
    p = Path(arg)
    errs = check(p)
    status = "OK" if not errs else f"{len(errs)} VIOLATIONS"
    print(f"{p.name}: {status}")
    for e in errs[:20]:
        print(f"  - {e}")
    fail = fail or bool(errs)
sys.exit(1 if fail else 0)
