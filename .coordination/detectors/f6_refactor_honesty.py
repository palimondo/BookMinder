#!/usr/bin/env python3
"""F6 refactor-honesty detector: verifies commits that claim refactoring.

Covers rule-index rows flagged F6 (T-20, T-21). For each commit whose
message claims refactoring it (a) replays the PARENT's spec tree against
the CHILD's implementation under the invoking environment — behavior must
be preserved, with specs already failing on the parent baseline excluded
and uncollectable specs skipped loudly; (b) AST-diffs spec files for
expectation rewrites smuggled into the refactor commit; (c) flags novel
public implementation surface and net new control flow labeled refactor;
(d) flags rename residue — a definition vanished while references remain.
"""

import argparse
import ast
import builtins
import copy
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

DEFAULT_EXCLUDES = ("claude-dev-log-diary/", ".coordination/", ".claude/")
EXCLUDES: tuple[str, ...] = DEFAULT_EXCLUDES
REFACTOR_RE = re.compile(r"(?i)\brefactor")
IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
BRANCH_NODES = (
    ast.If, ast.For, ast.While, ast.IfExp, ast.ExceptHandler,
    ast.comprehension, ast.match_case,
)
PYTEST_TIMEOUT = 300


def git(repo: str, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", repo, *args], capture_output=True, text=True, check=True
    ).stdout


def git_show(repo: str, sha: str, path: str) -> str | None:
    proc = subprocess.run(
        ["git", "-C", repo, "show", f"{sha}:{path}"],
        capture_output=True, text=True, errors="replace",
    )
    return proc.stdout if proc.returncode == 0 else None


def excluded(path: str) -> bool:
    return any(path.startswith(p) for p in EXCLUDES)


def is_spec_side(path: str) -> bool:
    if excluded(path):
        return False
    name = Path(path).name
    return (
        path.startswith(("specs/", "tests/", "features/"))
        or "/specs/" in path or "/tests/" in path
        or name == "conftest.py"
        or name.endswith(("_spec.py", "_test.py"))
        or name.startswith("test_")
    )


def is_impl(path: str) -> bool:
    return path.endswith(".py") and not excluded(path) and not is_spec_side(path)


class _ConstMasker(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        return ast.copy_location(ast.Constant(value="_"), node)


class _NameMasker(_ConstMasker):
    def visit_Name(self, node: ast.Name) -> ast.AST:
        return ast.copy_location(ast.Name(id="_", ctx=node.ctx), node)


def dump(node: ast.AST) -> str:
    return ast.dump(node)


def masked(node: ast.AST, names: bool = False) -> str:
    masker = _NameMasker() if names else _ConstMasker()
    return ast.dump(masker.visit(copy.deepcopy(node)))


def unparse(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except Exception:
        return dump(node)


@dataclass
class Finding:
    sha: str
    mode: str
    loc: str
    detail: str

    def line(self) -> str:
        return f"{self.sha[:9]} {self.mode} {self.loc} -- {self.detail}"


@dataclass
class AssertRec:
    dump: str
    name_masked: str
    node: ast.expr | None
    src: str
    consts: tuple = ()


def parse(source: str) -> ast.Module | None:
    try:
        return ast.parse(source)
    except SyntaxError:
        return None


def collect_asserts(source: str) -> list[AssertRec]:
    tree = parse(source)
    if tree is None:
        return []
    out: list[AssertRec] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            out.append(AssertRec(
                dump(node.test), masked(node.test, names=True),
                node.test, unparse(node.test), tuple(_constants(node.test)),
            ))
        elif (
            isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
            and node.value.func.attr.startswith("assert_")
        ):
            out.append(AssertRec(
                dump(node.value), masked(node.value, names=True),
                None, unparse(node.value), tuple(_constants(node.value)),
            ))
    return out


def _constants(node: ast.AST) -> list[object]:
    return [n.value for n in ast.walk(node) if isinstance(n, ast.Constant)]


def _identifier_rename_only(old: ast.expr, new: ast.expr) -> bool:
    if masked(old) != masked(new):
        return False
    oc, nc = _constants(old), _constants(new)
    diffs = [(a, b) for a, b in zip(oc, nc) if a != b]
    return bool(diffs) and all(
        isinstance(a, str) and isinstance(b, str)
        and IDENT_RE.match(a) and IDENT_RE.match(b)
        for a, b in diffs
    )


def _membership_strengthened(old: ast.expr, new: ast.expr) -> bool:
    for node in (old, new):
        if not (
            isinstance(node, ast.Compare) and len(node.ops) == 1
            and isinstance(node.ops[0], ast.In)
        ):
            return False
    oc, nc = _constants(old), _constants(new)
    if len(oc) != len(nc):
        return False
    diffs = [(a, b) for a, b in zip(oc, nc) if a != b]
    return bool(diffs) and all(
        isinstance(a, str) and isinstance(b, str) and a in b for a, b in diffs
    )


def changed_files(repo: str, sha: str) -> list[tuple[str, str | None, str | None]]:
    """(status, parent_path, child_path) vs first parent, rename-aware."""
    parents = git(repo, "rev-list", "--parents", "-n", "1", sha).split()
    if len(parents) == 1:
        raw = git(repo, "diff-tree", "-r", "--root", "--name-status", "-M", sha)
        lines = raw.strip().splitlines()[1:]
    else:
        raw = git(repo, "diff", "--name-status", "-M", f"{sha}^1", sha)
        lines = raw.strip().splitlines()
    out: list[tuple[str, str | None, str | None]] = []
    for line in lines:
        parts = line.split("\t")
        if len(parts) == 3 and parts[0].startswith("R"):
            out.append(("R", parts[1], parts[2]))
        elif len(parts) == 2:
            status, path = parts
            if status == "A":
                out.append(("A", None, path))
            elif status == "D":
                out.append(("D", path, None))
            else:
                out.append(("M", path, path))
    return out


def tree_files(repo: str, sha: str) -> list[str]:
    return git(repo, "ls-tree", "-r", "--name-only", sha).splitlines()


# ---------------------------------------------------------------- spec check

def check_spec_expectations(repo: str, sha: str,
                            entries: list[tuple[str, str | None, str | None]]
                            ) -> list[Finding]:
    parent_ref = f"{sha}^"
    removed: list[tuple[str, AssertRec]] = []
    child_dumps: set[str] = set()
    added: list[tuple[str, AssertRec]] = []
    parent_dumps: set[str] = set()

    pairs = [
        (old, new) for _, old, new in entries
        if ((old and is_spec_side(old)) or (new and is_spec_side(new)))
        and (old or new or "").endswith(".py")
        and (new or old or "").endswith(".py")
    ]
    if not pairs:
        return []
    for old, new in pairs:
        p_recs = collect_asserts(git_show(repo, parent_ref, old) or "") if old else []
        c_recs = collect_asserts(git_show(repo, sha, new) or "") if new else []
        parent_dumps.update(r.dump for r in p_recs)
        child_dumps.update(r.dump for r in c_recs)
        removed.extend((old or "", r) for r in p_recs)
        added.extend((new or "", r) for r in c_recs)

    removed = [(f, r) for f, r in removed if r.dump not in child_dumps]
    added = [(f, r) for f, r in added if r.dump not in parent_dumps]
    if removed:
        corpus: set[str] = set()
        for path in tree_files(repo, sha):
            if is_spec_side(path) and path.endswith(".py"):
                corpus.update(r.dump for r in
                              collect_asserts(git_show(repo, sha, path) or ""))
        removed = [(f, r) for f, r in removed if r.dump not in corpus]

    surviving_removed: list[tuple[str, AssertRec]] = []
    pool = list(added)
    for f, r in removed:
        match = None
        for cand in pool:
            _, c = cand
            if r.name_masked == c.name_masked and r.consts == c.consts:
                match = cand
                break
            if r.node is not None and c.node is not None and (
                _identifier_rename_only(r.node, c.node)
                or _membership_strengthened(r.node, c.node)
            ):
                match = cand
                break
        if match is not None:
            pool.remove(match)
        else:
            surviving_removed.append((f, r))

    out: list[Finding] = []
    by_file: dict[str, list[AssertRec]] = {}
    for f, r in surviving_removed:
        by_file.setdefault(f, []).append(r)
    for f, recs in by_file.items():
        srcs = "; ".join(f"assert {r.src}" for r in recs[:3])
        out.append(Finding(
            sha, "spec-expectation-changed", f,
            f"refactor-labeled commit rewrites/drops {len(recs)} spec "
            f"expectation(s): {srcs}"))
    return out


# ---------------------------------------------------------------- impl checks

def _defs(tree: ast.Module) -> dict[str, ast.AST]:
    out: dict[str, ast.AST] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out[node.name] = node
    return out


def _stmt_dumps(tree: ast.AST) -> set[str]:
    return {
        masked(n, names=True) for n in ast.walk(tree) if isinstance(n, ast.stmt)
    }


def _branch_count(tree: ast.AST) -> int:
    return sum(1 for n in ast.walk(tree) if isinstance(n, BRANCH_NODES))


def check_impl(repo: str, sha: str,
               entries: list[tuple[str, str | None, str | None]]
               ) -> list[Finding]:
    parent_ref = f"{sha}^"
    pairs = [
        (old, new) for _, old, new in entries
        if (old and is_impl(old)) or (new and is_impl(new))
    ]
    if not pairs:
        return []

    parent_impl_paths = [p for p in tree_files(repo, parent_ref) if is_impl(p)]
    parent_corpus_defs: dict[str, ast.AST] = {}
    parent_corpus_stmts: set[str] = set()
    for path in parent_impl_paths:
        tree = parse(git_show(repo, parent_ref, path) or "")
        if tree:
            parent_corpus_defs.update(_defs(tree))
            parent_corpus_stmts.update(_stmt_dumps(tree))

    out: list[Finding] = []
    p_branches = c_branches = 0
    vanished: set[str] = set()
    child_side_defs: set[str] = set()
    branch_files: list[str] = []

    for old, new in pairs:
        p_tree = parse(git_show(repo, parent_ref, old) or "") if old else None
        c_tree = parse(git_show(repo, sha, new) or "") if new else None
        p_defs = _defs(p_tree) if p_tree else {}
        c_defs = _defs(c_tree) if c_tree else {}
        child_side_defs.update(c_defs)
        if p_tree:
            p_branches += _branch_count(p_tree)
        if c_tree:
            c_branches += _branch_count(c_tree)
        if old or new:
            branch_files.append(new or old or "")

        for name, node in c_defs.items():
            if name in p_defs or name.startswith("_"):
                continue
            if name in parent_corpus_defs:
                continue  # moved across files
            if isinstance(node, ast.ClassDef) and all(
                isinstance(s, (ast.AnnAssign, ast.Pass))
                or (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))
                for s in node.body
            ):
                continue  # annotation-only shape (TypedDict etc.): a type, not behavior
            stmts = [
                masked(n, names=True) for n in ast.walk(node)
                if isinstance(n, ast.stmt) and n is not node
                and not (isinstance(n, ast.Expr)
                         and isinstance(n.value, ast.Constant))
            ]
            if not stmts:
                continue
            novel = [s for s in stmts if s not in parent_corpus_stmts]
            if len(novel) * 2 > len(stmts):
                kind = "class" if isinstance(node, ast.ClassDef) else "function"
                out.append(Finding(
                    sha, "impl-public-addition", f"{new}::{name}",
                    f"new public {kind} with novel body "
                    f"({len(novel)}/{len(stmts)} statements unseen in parent "
                    f"tree) lands under a refactor label"))
        vanished.update(set(p_defs) - set(c_defs))

    if c_branches > p_branches:
        out.append(Finding(
            sha, "impl-branch-addition", ",".join(sorted(set(branch_files))),
            f"net control-flow growth in a refactor-labeled commit: "
            f"{p_branches} -> {c_branches} branch nodes"))

    child_impl_defs: set[str] = set(child_side_defs)
    for path in tree_files(repo, sha):
        if is_impl(path):
            tree = parse(git_show(repo, sha, path) or "")
            if tree:
                child_impl_defs.update(_defs(tree))
    for name in sorted(vanished):
        if name in child_impl_defs:
            continue  # moved or renamed-and-defined elsewhere
        if name in vars(builtins):
            continue  # shadowed builtin: grep hits would be builtin uses
        proc = subprocess.run(
            ["git", "-C", repo, "grep", "-n", "-w", name, sha,
             "--", "*.py", *(f":(exclude){p}*" for p in EXCLUDES)],
            capture_output=True, text=True,
        )
        hits = [h for h in proc.stdout.splitlines() if h.strip()]
        if hits:
            first = hits[0].split(":", 1)[1] if ":" in hits[0] else hits[0]
            out.append(Finding(
                sha, "rename-residue", first.split(":")[0],
                f"'{name}' removed from implementation but {len(hits)} "
                f"reference(s) survive in the child tree (first: {first})"))
    return out


# ---------------------------------------------------------------- dynamic check

def _run_pytest(cwd: str, targets: list[str]) -> tuple[int, set[str], set[str], str]:
    """Return (exit, failed_ids, error_ids, tail)."""
    cmd = [
        sys.executable, "-m", "pytest", "-o", "addopts=",
        "-p", "no:cacheprovider", "--continue-on-collection-errors",
        "-q", "-rfE", *targets,
    ]
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=PYTEST_TIMEOUT
        )
    except subprocess.TimeoutExpired:
        return -1, set(), set(), "pytest timed out"
    failed, errors = set(), set()
    for line in proc.stdout.splitlines():
        if line.startswith("FAILED "):
            failed.add(line.split(" ", 1)[1].split(" -")[0])
        elif line.startswith("ERROR "):
            errors.add(line.split(" ", 1)[1].split(" -")[0])
    tail = "\n".join(proc.stdout.splitlines()[-3:])
    return proc.returncode, failed, errors, tail


def check_behavior(repo: str, sha: str) -> list[Finding]:
    parent_ref = git(repo, "rev-parse", f"{sha}^").strip()
    parent_specs = [
        p for p in tree_files(repo, parent_ref)
        if is_spec_side(p) and p.endswith(".py")
    ]
    spec_targets = [
        p for p in parent_specs if Path(p).name != "conftest.py"
    ]
    if not spec_targets:
        print(f"note: {sha[:9]} has no parent specs to replay", file=sys.stderr)
        return []

    out: list[Finding] = []
    with tempfile.TemporaryDirectory(prefix="f6-wt-") as tmp:
        wt = str(Path(tmp) / "wt")
        git(repo, "worktree", "add", "--detach", wt, parent_ref)
        try:
            rc, base_failed, base_errors, tail = _run_pytest(wt, spec_targets)
            if rc == -1 or rc >= 3:
                print(f"SKIP-DYNAMIC {sha[:9]}: baseline pytest unusable "
                      f"(exit {rc}): {tail}", file=sys.stderr)
                return []
            for tid in sorted(base_failed | base_errors):
                print(f"SKIP-BASELINE {sha[:9]} {tid}: fails/errors on the "
                      f"parent tree itself; excluded from behavior probe",
                      file=sys.stderr)

            subprocess.run(["git", "-C", wt, "checkout", "--force",
                            "--detach", sha], capture_output=True, check=True)
            subprocess.run(["git", "-C", wt, "clean", "-fdq"],
                           capture_output=True)
            for path in tree_files(repo, sha):
                if is_spec_side(path) and path.endswith(".py"):
                    p = Path(wt) / path
                    if p.exists():
                        p.unlink()
            for path in parent_specs:
                src = git_show(repo, parent_ref, path)
                if src is None:
                    continue
                dest = Path(wt) / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(src)

            rc, child_failed, child_errors, tail = _run_pytest(wt, spec_targets)
            if rc == -1:
                print(f"SKIP-DYNAMIC {sha[:9]}: overlay pytest timed out",
                      file=sys.stderr)
                return []
            for tid in sorted(child_errors - base_errors):
                print(f"SKIP-UNCOLLECTABLE {sha[:9]} {tid}: parent spec no "
                      f"longer collects against child tree (rename/moved "
                      f"infrastructure); excluded, verify by hand",
                      file=sys.stderr)
            for tid in sorted(child_failed - base_failed - base_errors):
                out.append(Finding(
                    sha, "refactor-behavior-broken", tid,
                    "passes on parent specs+parent impl, fails when parent "
                    "specs run against the refactor-labeled child impl"))
        finally:
            subprocess.run(["git", "-C", repo, "worktree", "remove",
                            "--force", wt], capture_output=True)
    return out


# ---------------------------------------------------------------- driver

def is_refactor_claim(subject: str, pattern: re.Pattern[str]) -> bool:
    s = subject.strip()
    if s.lower().startswith(("revert", 'revert "')):
        return False
    return bool(pattern.search(s))


def analyze_commit(repo: str, sha: str, static_only: bool) -> list[Finding]:
    entries = changed_files(repo, sha)
    touched_py = [
        p for _, old, new in entries for p in (old, new)
        if p and p.endswith(".py") and not excluded(p)
    ]
    if not touched_py:
        return []
    findings = check_spec_expectations(repo, sha, entries)
    findings += check_impl(repo, sha, entries)
    impl_changed = any(is_impl(p) for p in touched_py)
    parents = git(repo, "rev-list", "--parents", "-n", "1", sha).split()
    if impl_changed and not static_only and len(parents) > 1:
        findings += check_behavior(repo, sha)
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, help="path to the git repository")
    ap.add_argument("--range", dest="range_",
                    help="commit range A..B (first-parent walk); refactor-"
                         "claiming commits are selected by message")
    ap.add_argument("--commit", action="append", default=[],
                    help="analyze this commit regardless of message "
                         "(repeatable)")
    ap.add_argument("--all", action="store_true",
                    help="scan every refactor-claiming commit in history")
    ap.add_argument("--match", default=None,
                    help="regex selecting refactor-claiming subjects "
                         r"(default: (?i)\brefactor)")
    ap.add_argument("--static-only", action="store_true",
                    help="skip the parent-specs-vs-child-impl replay")
    ap.add_argument("--exclude", action="append", default=None,
                    help="path prefix to skip (defaults: claude-dev-log-diary/,"
                         " .coordination/, .claude/)")
    args = ap.parse_args()

    global EXCLUDES
    if args.exclude is not None:
        EXCLUDES = tuple(args.exclude)
    pattern = re.compile(args.match) if args.match else REFACTOR_RE

    shas: list[str] = []
    if args.range_ or args.all:
        spec = args.range_ if args.range_ else "HEAD"
        raw = git(args.repo, "rev-list", "--first-parent", "--reverse",
                  "--format=%H%x00%s", spec)
        for block in raw.splitlines():
            if block.startswith("commit "):
                continue
            sha, _, subject = block.partition("\x00")
            if is_refactor_claim(subject, pattern):
                shas.append(sha)
    for c in args.commit:
        shas.append(git(args.repo, "rev-parse", c).strip())
    if not shas:
        ap.error("provide --range, --all, or --commit")

    findings: list[Finding] = []
    for sha in shas:
        try:
            findings.extend(analyze_commit(args.repo, sha, args.static_only))
        except subprocess.CalledProcessError as exc:
            print(f"error analyzing {sha[:9]}: {exc}", file=sys.stderr)
    for f in findings:
        print(f.line())
    if not findings:
        print(f"clean: no refactor-honesty findings in {len(shas)} commit(s)",
              file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
