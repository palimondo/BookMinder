#!/usr/bin/env python3
"""F3 minimality residue detector (mutation-lite).

The 100% coverage gate is the primary F3 detector (author ruling); this tool
detects the residue the gate cannot see: code that specs EXECUTE but no
assertion FORCES. Method: sample cheap mutants over executed implementation
lines, run the suite per mutant, report survivors with the nearest covering
spec context.

Exit codes: 0 clean, 1 findings (survivors), 2 operational error.
"""

import argparse
import ast
import configparser
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "claude-dev-log-diary",
    ".coordination",
    "htmlcov",
}

COMPARE_SWAP = {
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
    ast.Lt: ast.GtE,
    ast.GtE: ast.Lt,
    ast.Gt: ast.LtE,
    ast.LtE: ast.Gt,
    ast.In: ast.NotIn,
    ast.NotIn: ast.In,
    ast.Is: ast.IsNot,
    ast.IsNot: ast.Is,
}

FAILURE_NAMES = {
    "invert-conditional": "unforced-branch",
    "delete-branch-body": "unforced-branch-body",
    "swap-comparison": "unforced-comparison",
    "swap-constant": "unforced-constant",
}


class Site:
    def __init__(self, kind, index, lineno, stmt_lineno, func, desc):
        self.kind = kind
        self.index = index
        self.lineno = lineno
        self.stmt_lineno = stmt_lineno
        self.func = func
        self.desc = desc


class SiteCollector(ast.NodeVisitor):
    """Enumerate mutation sites in deterministic order, skipping docstrings
    and annotation subtrees."""

    def __init__(self):
        self.sites = []
        self.counters = {}
        self.func_stack = ["<module>"]
        self.stmt_lineno = 0
        self.docstrings = set()

    def _add(self, kind, lineno, desc):
        idx = self.counters.get(kind, 0)
        self.counters[kind] = idx + 1
        self.sites.append(
            Site(kind, idx, lineno, self.stmt_lineno, self.func_stack[-1], desc)
        )
        return idx

    def _note_docstring(self, node):
        body = getattr(node, "body", [])
        if (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            self.docstrings.add(id(body[0].value))

    def visit(self, node):
        if isinstance(node, ast.stmt):
            self.stmt_lineno = node.lineno
        if isinstance(node, ast.Module | ast.ClassDef):
            self._note_docstring(node)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            self._note_docstring(node)
            self.func_stack.append(node.name)
            self._generic_visit_skip_annotations(node)
            self.func_stack.pop()
            return
        self._collect(node)
        self._generic_visit_skip_annotations(node)

    def _generic_visit_skip_annotations(self, node):
        for field, value in ast.iter_fields(node):
            if field in ("annotation", "returns"):
                continue
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)

    def _collect(self, node):
        if isinstance(node, ast.If | ast.IfExp):
            self._add("invert-conditional", node.lineno, "if <test> -> if not(<test>)")
            if isinstance(node, ast.If):
                self._add("delete-branch-body", node.lineno, "if body -> pass")
        elif isinstance(node, ast.Compare):
            for op in node.ops:
                if type(op) in COMPARE_SWAP:
                    self._add(
                        "swap-comparison",
                        node.lineno,
                        f"{type(op).__name__} -> {COMPARE_SWAP[type(op)].__name__}",
                    )
                else:
                    self.counters["swap-comparison"] = (
                        self.counters.get("swap-comparison", 0) + 1
                    )
        elif isinstance(node, ast.Constant) and id(node) not in self.docstrings:
            v = node.value
            if v is True or v is False:
                self._add("swap-constant", node.lineno, f"{v} -> {not v}")
            elif isinstance(v, int | float) and not isinstance(v, bool):
                self._add("swap-constant", node.lineno, f"{v} -> {v + 1}")
            elif isinstance(v, str) and v:
                self._add("swap-constant", node.lineno, f"{v!r} -> {v + 'XX'!r}")
            else:
                self.counters["swap-constant"] = (
                    self.counters.get("swap-constant", 0) + 1
                )


class Mutator(ast.NodeTransformer):
    """Apply the mutation at the nth site of the given kind, walking the tree
    in the same order as SiteCollector."""

    def __init__(self, kind, target_index):
        self.kind = kind
        self.target = target_index
        self.count = 0
        self.applied = False
        self.docstrings = set()

    def _note_docstring(self, node):
        body = getattr(node, "body", [])
        if (
            body
            and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)
        ):
            self.docstrings.add(id(body[0].value))

    def _hit(self):
        hit = self.count == self.target
        self.count += 1
        return hit

    def visit(self, node):
        if isinstance(
            node, ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef
        ):
            self._note_docstring(node)
        node = self._mutate(node)
        for field, value in ast.iter_fields(node):
            if field in ("annotation", "returns"):
                continue
            if isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, ast.AST):
                        new_list.append(self.visit(item))
                    else:
                        new_list.append(item)
                value[:] = new_list
            elif isinstance(value, ast.AST):
                setattr(node, field, self.visit(value))
        return node

    def _mutate(self, node):
        kind = self.kind
        if isinstance(node, ast.If | ast.IfExp):
            if kind == "invert-conditional" and self._count_kind("invert-conditional"):
                node.test = ast.UnaryOp(op=ast.Not(), operand=node.test)
                self.applied = True
            if isinstance(node, ast.If) and kind == "delete-branch-body":
                if self._count_kind("delete-branch-body"):
                    node.body = [ast.Pass()]
                    self.applied = True
        elif isinstance(node, ast.Compare):
            for i, op in enumerate(node.ops):
                if type(op) in COMPARE_SWAP:
                    if kind == "swap-comparison" and self._count_kind(
                        "swap-comparison"
                    ):
                        node.ops[i] = COMPARE_SWAP[type(op)]()
                        self.applied = True
                elif kind == "swap-comparison":
                    self.count += 1
        elif isinstance(node, ast.Constant) and id(node) not in self.docstrings:
            v = node.value
            mutable = (
                v is True
                or v is False
                or (isinstance(v, int | float) and not isinstance(v, bool))
                or (isinstance(v, str) and v)
            )
            if kind == "swap-constant":
                if mutable and self._count_kind("swap-constant"):
                    if v is True or v is False:
                        node.value = not v
                    elif isinstance(v, int | float):
                        node.value = v + 1
                    else:
                        node.value = v + "XX"
                    self.applied = True
                elif not mutable:
                    self.count += 1
        return node

    def _count_kind(self, kind):
        if self.kind != kind:
            return False
        return self._hit()


def copy_tree(src: Path, dst: Path):
    def ignore(directory, names):
        return [n for n in names if n in IGNORE_DIRS or n.endswith(".egg-info")]

    shutil.copytree(src, dst, ignore=ignore, symlinks=True, dirs_exist_ok=True)


def run_pytest(workdir: Path, extra=(), timeout=300):
    cmd = [sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider"]
    cmd += list(extra)
    env = dict(os.environ)
    # All same-size mutants of a file collide in CPython's (mtime-seconds,
    # size) pyc invalidation check when runs are sub-second, so a stale pyc
    # would silently execute the PREVIOUS mutant. No bytecode cache, ever.
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        cmd, cwd=workdir, capture_output=True, text=True, timeout=timeout, env=env
    )


def collect_coverage(workdir: Path, package: str):
    rc = workdir / ".f3_coveragerc"
    cp = configparser.ConfigParser()
    cp["run"] = {}
    cp["json"] = {"show_contexts": "true"}
    with open(rc, "w") as f:
        cp.write(f)
    out = workdir / ".f3_cov.json"
    r = run_pytest(
        workdir,
        [
            f"--cov={package}",
            "--cov-context=test",
            f"--cov-report=json:{out}",
            f"--cov-config={rc}",
        ],
    )
    if r.returncode != 0 or not out.exists():
        return None, r
    with open(out) as f:
        return json.load(f), r


def enumerate_sites(workdir: Path, package: str, cov: dict):
    files = {}
    for path in sorted((workdir / package).rglob("*.py")):
        rel = path.relative_to(workdir).as_posix()
        covfile = cov["files"].get(rel)
        if covfile is None:
            continue
        executed = set(covfile["executed_lines"])
        contexts = covfile.get("contexts", {})
        src = path.read_text()
        collector = SiteCollector()
        collector.visit(ast.parse(src))
        sites = [s for s in collector.sites if s.stmt_lineno in executed]
        if sites:
            files[rel] = (sites, contexts)
    return files


def sample(files: dict, per_function_cap: int, max_mutants: int):
    picked = []
    per_func = {}
    for rel in sorted(files):
        sites, _ = files[rel]
        for s in sorted(sites, key=lambda s: (s.lineno, s.kind, s.index)):
            key = (rel, s.func)
            if per_func.get(key, 0) >= per_function_cap:
                continue
            per_func[key] = per_func.get(key, 0) + 1
            picked.append((rel, s))
    return picked[:max_mutants]


def spec_context(contexts: dict, lineno: int) -> str:
    ctx = sorted(c for c in contexts.get(str(lineno), []) if c)
    if ctx:
        return ctx[0].split("|")[0]
    return "(import-time only; no test context)"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, help="repo root to analyze")
    ap.add_argument("--package", default="bookminder", help="implementation package")
    ap.add_argument("--max-mutants", type=int, default=60)
    ap.add_argument("--per-function-cap", type=int, default=4)
    ap.add_argument("--keep-workdir", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not (repo / args.package).is_dir():
        print(f"error: package dir not found: {repo / args.package}", file=sys.stderr)
        return 2

    tmp = Path(tempfile.mkdtemp(prefix="f3_residue_"))
    workdir = tmp / "tree"
    try:
        copy_tree(repo, workdir)

        t0 = time.monotonic()
        baseline = run_pytest(workdir)
        baseline_secs = time.monotonic() - t0
        if baseline.returncode != 0:
            print(
                "error: baseline suite is not green; residue is undefined on a "
                "red suite",
                file=sys.stderr,
            )
            print(baseline.stdout[-2000:], file=sys.stderr)
            return 2
        mutant_timeout = max(10, int(baseline_secs * 5) + 5)

        cov, covrun = collect_coverage(workdir, args.package)
        if cov is None:
            print("error: coverage collection failed", file=sys.stderr)
            print(covrun.stdout[-2000:], file=sys.stderr)
            return 2

        files = enumerate_sites(workdir, args.package, cov)
        picked = sample(files, args.per_function_cap, args.max_mutants)
        if args.verbose:
            total = sum(len(s) for s, _ in files.values())
            print(
                f"# baseline {baseline_secs:.2f}s; {total} executed-line sites, "
                f"{len(picked)} sampled (cap {args.per_function_cap}/function, "
                f"{args.max_mutants} total); per-mutant timeout {mutant_timeout}s",
                file=sys.stderr,
            )

        survivors = []
        for rel, site in picked:
            path = workdir / rel
            original = path.read_text()
            mut = Mutator(site.kind, site.index)
            tree = mut.visit(ast.parse(original))
            if not mut.applied:
                continue
            ast.fix_missing_locations(tree)
            path.write_text(ast.unparse(tree) + "\n")
            try:
                r = run_pytest(workdir, timeout=mutant_timeout)
                killed = r.returncode != 0
            except subprocess.TimeoutExpired:
                killed = True
            finally:
                path.write_text(original)
            if not killed:
                _, contexts = files[rel]
                survivors.append((rel, site, spec_context(contexts, site.stmt_lineno)))
            if args.verbose:
                status = "SURVIVED" if not killed else "killed"
                print(
                    f"# {rel}:{site.lineno} {site.kind} [{site.desc}] {status}",
                    file=sys.stderr,
                )

        for rel, site, ctx in survivors:
            print(
                f"{FAILURE_NAMES[site.kind]}: {rel}:{site.lineno} in {site.func}() "
                f"— mutant [{site.desc}] survived the full suite; "
                f"nearest covering spec: {ctx}"
            )
        if survivors:
            print(
                f"# {len(survivors)}/{len(picked)} sampled mutants survived: "
                "executed-but-unforced code (F3 residue)",
                file=sys.stderr,
            )
            return 1
        print(
            f"# clean: all {len(picked)} sampled mutants killed by the suite",
            file=sys.stderr,
        )
        return 0
    finally:
        if args.keep_workdir:
            print(f"# workdir kept: {workdir}", file=sys.stderr)
        else:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
