#!/usr/bin/env python3
"""F2 assertion-integrity detector: git-DAG + AST checks over spec files.

Covers rule-index rows flagged F2 (T-51..T-55, T-57..T-60, T-64, T-91) and
ledger L-01 both-rules. For each commit in a range, AST-diffs every spec file
between first-parent and child, pairing it_ functions by name (same file or
cross-file, so "pure move" rewrites like e5c7074 are diffed, not trusted),
and runs static integrity checks on new/modified spec bodies.
"""

import argparse
import ast
import subprocess
import sys
from dataclasses import dataclass, field

SPEC_SUFFIXES = ("_spec.py", "_test.py")
GUARD_GT = {"Gt": 0, "GtE": 1, "NotEq": 0}
EMPTY_NAME_WORDS = (
    "empty", "no_", "none", "without", "missing", "not_", "excludes", "zero"
)


DEFAULT_EXCLUDES = ("claude-dev-log-diary/",)
EXCLUDES: tuple[str, ...] = DEFAULT_EXCLUDES


def is_spec_path(path: str) -> bool:
    if any(path.startswith(p) for p in EXCLUDES):
        return False
    return path.endswith(SPEC_SUFFIXES)


def git(repo: str, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", repo, *args], capture_output=True, text=True, check=True
    ).stdout


def git_show(repo: str, sha: str, path: str) -> str | None:
    proc = subprocess.run(
        ["git", "-C", repo, "show", f"{sha}:{path}"], capture_output=True, text=True
    )
    return proc.stdout if proc.returncode == 0 else None


def dump(node: ast.AST) -> str:
    return ast.dump(node)


class _ConstMasker(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        return ast.copy_location(ast.Constant(value="_"), node)


def masked_dump(node: ast.AST) -> str:
    import copy

    return ast.dump(_ConstMasker().visit(copy.deepcopy(node)))


def unparse(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except Exception:
        return dump(node)


@dataclass
class AssertRec:
    test: ast.expr
    dump: str
    masked: str
    src: str
    lineno: int
    in_loop: bool = False
    in_if: bool = False


@dataclass
class Fn:
    file: str
    qual: str
    name: str
    node: ast.FunctionDef
    body_dump: str
    asserts: list[AssertRec] = field(default_factory=list)
    mock_asserts: list[str] = field(default_factory=list)
    patch_count: int = 0
    return_value_dumps: list[str] = field(default_factory=list)
    return_value_set: bool = False
    side_effect_set: bool = False
    has_skip: bool = False
    all_strings: list[str] = field(default_factory=list)

    @property
    def loc(self) -> str:
        return f"{self.file}::{self.qual}"


def _is_skip_decorator(dec: ast.expr) -> bool:
    text = unparse(dec)
    return any(m in text for m in ("mark.skip", "mark.xfail", "mark.skipif"))


def _collect(fn: Fn, stmts: list[ast.stmt], in_loop: bool, in_if: bool) -> None:
    for stmt in stmts:
        if isinstance(stmt, ast.Assert):
            fn.asserts.append(
                AssertRec(
                    stmt.test, dump(stmt.test), masked_dump(stmt.test),
                    unparse(stmt.test), stmt.lineno, in_loop, in_if,
                )
            )
        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            call = stmt.value
            if isinstance(call.func, ast.Attribute):
                if call.func.attr.startswith("assert_"):
                    fn.mock_asserts.append(dump(call))
                if (
                    isinstance(call.func.value, ast.Name)
                    and call.func.value.id == "pytest"
                    and call.func.attr in ("skip", "xfail")
                ):
                    fn.has_skip = True
        elif isinstance(stmt, ast.Assign):
            for tgt in stmt.targets:
                if isinstance(tgt, ast.Attribute):
                    if tgt.attr == "return_value":
                        fn.return_value_set = True
                        fn.return_value_dumps.append(dump(stmt.value))
                    elif tgt.attr == "side_effect":
                        fn.side_effect_set = True
        for child in ast.iter_child_nodes(stmt):
            if isinstance(child, ast.Call):
                pass
        if isinstance(stmt, (ast.For, ast.While)):
            _collect(fn, stmt.body, True, in_if)
            _collect(fn, stmt.orelse, True, in_if)
        elif isinstance(stmt, ast.If):
            _collect(fn, stmt.body, in_loop, True)
            _collect(fn, stmt.orelse, in_loop, True)
        elif isinstance(stmt, (ast.With, ast.Try)):
            for group in (
                getattr(stmt, "body", []),
                getattr(stmt, "orelse", []),
                getattr(stmt, "finalbody", []),
            ):
                _collect(fn, group, in_loop, in_if)
            for handler in getattr(stmt, "handlers", []):
                _collect(fn, handler.body, in_loop, in_if)


def analyze_fn(file: str, qual: str, node: ast.FunctionDef) -> Fn:
    body_dump = dump(ast.Module(body=node.body, type_ignores=[])) + "".join(
        dump(d) for d in node.decorator_list
    )
    fn = Fn(file, qual, node.name, node, body_dump)
    fn.has_skip = any(_is_skip_decorator(d) for d in node.decorator_list)
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call):
            f = sub.func
            if (isinstance(f, ast.Name) and f.id == "patch") or (
                isinstance(f, ast.Attribute) and f.attr in ("patch", "object")
                and "patch" in unparse(f)
            ):
                fn.patch_count += 1
                for kw in sub.keywords:
                    if kw.arg == "return_value":
                        fn.return_value_set = True
                        fn.return_value_dumps.append(dump(kw.value))
                    elif kw.arg == "side_effect":
                        fn.side_effect_set = True
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            fn.all_strings.append(sub.value)
    _collect(fn, node.body, False, False)
    return fn


def index_specs(file: str, source: str) -> tuple[dict[str, Fn], set[str]]:
    """Index it_/test_ functions plus every assert dump in the file (helpers
    included), so assertions relocated into shared helpers are not counted
    as removed."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}, set()
    out: dict[str, Fn] = {}
    file_assert_dumps = {
        dump(n.test) for n in ast.walk(tree) if isinstance(n, ast.Assert)
    }

    def walk(node: ast.AST, prefix: str) -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qual = f"{prefix}{child.name}"
                if child.name.startswith(("it_", "test_")):
                    out[qual] = analyze_fn(file, qual, child)
                walk(child, qual + "::")
            elif isinstance(child, ast.ClassDef):
                walk(child, f"{prefix}{child.name}::")

    walk(tree, "")
    return out, file_assert_dumps


def _len_compare(test: ast.expr) -> tuple[str, ast.expr, int] | None:
    """Return (op, subject, n) when test is len(subject) <op> n (either order)."""
    if not (isinstance(test, ast.Compare) and len(test.ops) == 1):
        return None
    left, op, right = test.left, test.ops[0], test.comparators[0]
    for a, b, flip in ((left, right, False), (right, left, True)):
        if (
            isinstance(a, ast.Call)
            and isinstance(a.func, ast.Name)
            and a.func.id == "len"
            and a.args
            and isinstance(b, ast.Constant)
            and isinstance(b.value, int)
        ):
            name = type(op).__name__
            if flip:
                name = {"Gt": "Lt", "Lt": "Gt", "GtE": "LtE", "LtE": "GtE"}.get(name, name)
            return name, a.args[0], b.value
    return None


def is_guard(rec: AssertRec) -> bool:
    lc = _len_compare(rec.test)
    if lc and GUARD_GT.get(lc[0]) == lc[2]:
        return True
    return isinstance(rec.test, (ast.Name, ast.Attribute))


def is_truthiness(test: ast.expr) -> bool:
    return isinstance(test, (ast.Name, ast.Attribute))


@dataclass
class Finding:
    sha: str
    mode: str
    loc: str
    detail: str

    def line(self) -> str:
        return f"{self.sha[:9]} {self.mode} {self.loc} -- {self.detail}"


def static_findings(fn: Fn) -> list[tuple[str, str]]:
    """Return (mode, detail) pairs for one function body, commit-independent."""
    out: list[tuple[str, str]] = []
    for rec in fn.asserts:
        if isinstance(rec.test, ast.BoolOp) and isinstance(rec.test.op, ast.Or):
            out.append(
                ("disjunctive-assertion",
                 f"passes under alternative outcomes: assert {rec.src}")
            )
        lc = _len_compare(rec.test)
        if lc:
            op, subject, n = lc
            if op in ("Gt", "GtE", "Eq") and n >= 1 and GUARD_GT.get(op) != n:
                out.append(
                    ("fixture-cardinality-contract",
                     f"behavioral contract encoded as count: assert {rec.src}")
                )
    if fn.return_value_set and not fn.side_effect_set:
        for rec in fn.asserts:
            t = rec.test
            if (
                isinstance(t, ast.Compare)
                and len(t.ops) == 1
                and isinstance(t.ops[0], ast.NotIn)
                and isinstance(t.left, ast.Constant)
                and isinstance(t.left.value, str)
            ):
                needle = t.left.value
                others = [
                    s for s in fn.all_strings
                    if s != needle and s not in rec.src
                ]
                if not any(needle in s for s in others):
                    out.append(
                        ("mock-guaranteed-absence",
                         f"stub never supplies '{needle}'; absence assertion "
                         f"cannot fail: assert {rec.src}")
                    )
            if isinstance(t, ast.Compare) and len(t.ops) == 1 and isinstance(
                t.ops[0], (ast.Eq, ast.Is)
            ):
                sides = {dump(t.left), dump(t.comparators[0])}
                if sides & set(fn.return_value_dumps):
                    out.append(
                        ("tautological-mock-echo",
                         f"asserts the value the mock supplies: assert {rec.src}")
                    )
    conditioned = [r for r in fn.asserts if r.in_loop or r.in_if]
    if conditioned and fn.asserts:
        guards = [r for r in fn.asserts if not (r.in_loop or r.in_if) and is_guard(r)]
        unconditional = [
            r for r in fn.asserts if not (r.in_loop or r.in_if) and not is_guard(r)
        ]
        if not guards and not unconditional and not fn.mock_asserts:
            out.append(
                ("unguarded-conditional-assertion",
                 "every assertion sits inside a loop/conditional with no "
                 "non-emptiness guard; passes vacuously on empty output")
            )
    real_asserts = fn.asserts + [
        AssertRec(ast.Constant(value=0), d, d, d, 0) for d in fn.mock_asserts
    ]
    if len(fn.asserts) == 1 and not fn.mock_asserts:
        rec = fn.asserts[0]
        t = rec.test
        empty = False
        if isinstance(t, ast.UnaryOp) and isinstance(t.op, ast.Not):
            empty = True
        lc = _len_compare(t)
        if lc and lc[0] == "Eq" and lc[2] == 0:
            empty = True
        if (
            isinstance(t, ast.Compare)
            and len(t.ops) == 1
            and isinstance(t.ops[0], ast.Eq)
        ):
            for side in (t.left, t.comparators[0]):
                if (isinstance(side, (ast.List, ast.Dict, ast.Tuple)) and not getattr(
                    side, "elts", getattr(side, "keys", [1])
                )) or (isinstance(side, ast.Constant) and side.value == ""):
                    empty = True
        if empty and not any(w in fn.name.lower() for w in EMPTY_NAME_WORDS):
            out.append(
                ("emptiness-as-expectation",
                 f"sole assertion pins emptiness under a name promising "
                 f"behavior: assert {rec.src}")
            )
    return out


def _constants(node: ast.AST) -> list[object]:
    return [n.value for n in ast.walk(node) if isinstance(n, ast.Constant)]


IDENT_RE = __import__("re").compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _identifier_rename_only(old: ast.expr, new: ast.expr) -> bool:
    """True when the only differing constants are identifier-like strings on
    both sides (a coordinated field/key rename, not an expectation rewrite)."""
    oc, nc = _constants(old), _constants(new)
    if len(oc) != len(nc):
        return False
    diffs = [(a, b) for a, b in zip(oc, nc) if a != b]
    return bool(diffs) and all(
        isinstance(a, str) and isinstance(b, str)
        and IDENT_RE.match(a) and IDENT_RE.match(b)
        for a, b in diffs
    )


def _membership_strengthened(old: ast.expr, new: ast.expr) -> bool:
    """True when both are `needle in haystack` asserts and every changed
    string constant grew to contain its old value (a stricter needle)."""
    for node in (old, new):
        if not (
            isinstance(node, ast.Compare)
            and len(node.ops) == 1
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


def diff_pair(
    sha: str, parent: Fn, child: Fn, moved: bool, child_file_dumps: set[str]
) -> list[Finding]:
    out: list[Finding] = []
    loc = child.loc + (f" (was {parent.file})" if moved else "")
    p_dumps = [r.dump for r in parent.asserts] + parent.mock_asserts
    c_dumps = [r.dump for r in child.asserts] + child.mock_asserts
    removed = [
        d for d in p_dumps if d not in c_dumps and d not in child_file_dumps
    ]
    added = [d for d in c_dumps if d not in p_dumps]

    if child.has_skip and not parent.has_skip:
        out.append(Finding(sha, "skip-to-restore-green", loc,
                           "existing spec gained a skip marker"))

    if removed and not added:
        srcs = [r.src for r in parent.asserts if r.dump in removed] or removed
        out.append(Finding(sha, "assertion-removed", loc,
                           "dropped without replacement: " + "; ".join(
                               f"assert {s}" for s in srcs[:3])))

    p_masked = {r.masked: r for r in parent.asserts}
    for rec in child.asserts:
        if rec.dump in p_dumps:
            continue
        twin = p_masked.get(rec.masked)
        if (
            twin and twin.dump != rec.dump and twin.dump in removed
            and not _identifier_rename_only(twin.test, rec.test)
            and not _membership_strengthened(twin.test, rec.test)
        ):
            out.append(Finding(sha, "literal-swap-same-name", loc,
                               f"expected value changed under unchanged it_ name: "
                               f"'assert {twin.src}' -> 'assert {rec.src}'"))
        if isinstance(rec.test, ast.BoolOp) and isinstance(rec.test.op, ast.Or):
            out.append(Finding(sha, "disjunction-added", loc,
                               f"assert {rec.src}"))

    for prec in parent.asserts:
        t = prec.test
        if not (isinstance(t, ast.Compare) and len(t.ops) == 1
                and isinstance(t.ops[0], ast.Eq)):
            continue
        sides = {dump(t.left), dump(t.comparators[0])}
        if prec.dump in c_dumps:
            continue
        for crec in child.asserts:
            if crec.dump in p_dumps:
                continue
            ct = crec.test
            if isinstance(ct, ast.Compare) and len(ct.ops) == 1:
                if isinstance(ct.ops[0], ast.In) and (
                    dump(ct.left) in sides
                    or dump(ct.comparators[0]) in sides
                ):
                    out.append(Finding(sha, "equality-relaxed", loc,
                                       f"'assert {prec.src}' -> membership "
                                       f"'assert {crec.src}'"))
                lc = _len_compare(ct)
                if lc and dump(lc[1]) in sides:
                    out.append(Finding(sha, "exact-set-relaxed-to-cardinality", loc,
                                       f"'assert {prec.src}' -> "
                                       f"'assert {crec.src}'"))
            if is_truthiness(ct) and dump(ct) in sides:
                out.append(Finding(sha, "equality-relaxed", loc,
                                   f"'assert {prec.src}' -> truthiness "
                                   f"'assert {crec.src}'"))

    def _exact_nonempty_eq(rec: AssertRec) -> bool:
        t = rec.test
        if not (isinstance(t, ast.Compare) and len(t.ops) == 1
                and isinstance(t.ops[0], ast.Eq)):
            return False
        return any(
            isinstance(s, (ast.List, ast.Set, ast.Tuple)) and s.elts
            or isinstance(s, ast.Dict) and s.keys
            for s in (t.left, t.comparators[0])
        )

    parent_guard = any(is_guard(r) for r in parent.asserts)
    child_guard = any(
        is_guard(r) or _exact_nonempty_eq(r) for r in child.asserts
    )
    if parent_guard and not child_guard and parent.asserts and child.asserts:
        out.append(Finding(sha, "nonemptiness-guard-removed", loc,
                           "parent version guarded against empty output; "
                           "child version does not"))

    if parent.patch_count == 0 and child.patch_count > 0 and child.return_value_set:
        out.append(Finding(sha, "mock-swapped-under-same-name", loc,
                           "real-collaborator spec replaced by mock-fed spec "
                           "under an unchanged it_ name"))
    return out


def changed_spec_files(repo: str, sha: str) -> list[tuple[str, str | None, str | None]]:
    """(status, parent_path, child_path) for spec files changed vs first parent."""
    parents = git(repo, "rev-list", "--parents", "-n", "1", sha).split()
    entries: list[tuple[str, str | None, str | None]] = []
    if len(parents) == 1:
        raw = git(repo, "diff-tree", "-r", "--root", "--name-status", "-M", sha)
        lines = raw.strip().splitlines()[1:]
    else:
        raw = git(repo, "diff", "--name-status", "-M", f"{sha}^1", sha)
        lines = raw.strip().splitlines()
    for line in lines:
        if not line.strip():
            continue
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("R") and len(parts) == 3:
            old, new = parts[1], parts[2]
            if is_spec_path(old) or is_spec_path(new):
                entries.append(("R", old, new))
        elif len(parts) == 2:
            path = parts[1]
            if not is_spec_path(path):
                continue
            if status == "A":
                entries.append(("A", None, path))
            elif status == "D":
                entries.append(("D", path, None))
            else:
                entries.append(("M", path, path))
    return entries


def analyze_commit(repo: str, sha: str, run_static: bool) -> list[Finding]:
    entries = changed_spec_files(repo, sha)
    if not entries:
        return []
    parent_ref, child_ref = f"{sha}^", sha
    parent_idx: dict[str, dict[str, Fn]] = {}
    child_idx: dict[str, dict[str, Fn]] = {}
    child_dumps: dict[str, set[str]] = {}
    for status, old, new in entries:
        if old is not None:
            src = git_show(repo, parent_ref, old)
            parent_idx[old] = index_specs(old, src)[0] if src else {}
        if new is not None:
            src = git_show(repo, child_ref, new)
            child_idx[new], child_dumps[new] = (
                index_specs(new, src) if src else ({}, set())
            )

    findings: list[Finding] = []
    child_by_name: dict[str, list[Fn]] = {}
    for funcs in child_idx.values():
        for fn in funcs.values():
            child_by_name.setdefault(fn.name, []).append(fn)

    matched_child: set[tuple[str, str]] = set()
    for status, old, new in entries:
        if old is None:
            continue
        for qual, pfn in parent_idx[old].items():
            cfn = child_idx.get(new or "", {}).get(qual) if new else None
            moved = False
            if cfn is None:
                candidates = [
                    c for c in child_by_name.get(pfn.name, [])
                    if (c.file, c.qual) not in matched_child
                ]
                if candidates:
                    cfn = candidates[0]
                    moved = cfn.file != old or cfn.qual != qual
            if cfn is None:
                continue
            matched_child.add((cfn.file, cfn.qual))
            if pfn.body_dump == cfn.body_dump:
                continue
            findings.extend(
                diff_pair(sha, pfn, cfn, moved,
                          child_dumps.get(cfn.file, set()))
            )
            if run_static:
                p_static = set(static_findings(pfn))
                for mode, detail in static_findings(cfn):
                    if (mode, detail) not in p_static:
                        findings.append(Finding(sha, mode, cfn.loc, detail))

    if run_static:
        touches_production = any(
            not is_spec_path(p) and p.endswith(".py") and "conftest" not in p
            for p in git(
                repo, "diff-tree", "-r", "--root", "--name-only", sha
            ).strip().splitlines()[1:]
        )
        for funcs in child_idx.values():
            for fn in funcs.values():
                if (fn.file, fn.qual) in matched_child:
                    continue
                if any(fn.qual in pidx for pidx in parent_idx.values()):
                    continue
                for mode, detail in static_findings(fn):
                    findings.append(Finding(sha, mode, fn.loc, detail))
                if fn.has_skip and touches_production:
                    findings.append(Finding(
                        sha, "skip-as-stand-in", fn.loc,
                        "new skipped spec committed beside production changes"))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, help="path to the git repository")
    ap.add_argument("--range", dest="range_",
                    help="commit range A..B (first-parent walk)")
    ap.add_argument("--commit", action="append", default=[],
                    help="single commit to analyze (repeatable)")
    ap.add_argument("--no-static", action="store_true",
                    help="diff-based weakening checks only")
    ap.add_argument("--exclude", action="append", default=None,
                    help="path prefix to skip (default: claude-dev-log-diary/)")
    args = ap.parse_args()

    global EXCLUDES
    if args.exclude is not None:
        EXCLUDES = tuple(args.exclude)

    shas: list[str] = []
    if args.range_:
        shas.extend(
            git(args.repo, "rev-list", "--first-parent", "--reverse",
                args.range_).split()
        )
    for c in args.commit:
        shas.append(git(args.repo, "rev-parse", c).strip())
    if not shas:
        ap.error("provide --range or --commit")

    findings: list[Finding] = []
    for sha in shas:
        try:
            findings.extend(analyze_commit(args.repo, sha, not args.no_static))
        except subprocess.CalledProcessError as exc:
            print(f"error analyzing {sha[:9]}: {exc}", file=sys.stderr)
    for f in findings:
        print(f.line())
    if not findings:
        print(f"clean: no assertion-integrity findings in {len(shas)} commit(s)",
              file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
