#!/usr/bin/env python3
"""F4 layering-and-seams detector: static checks over one tree state.

Covers the F4-flagged rules of the tdd-bdd rule index (T-61, T-66, T-67,
T-69, T-70, T-71, T-72, T-74) plus ledger L-09. Each finding prints as one
line: <failure-mode>: <path>:<line> <detail> (rule).

Run against the working tree:  python3 f4_layering.py --repo /path/to/repo
Run against a revision:        python3 f4_layering.py --repo /path/to/repo --rev <sha>
Exit 0 clean, 1 findings.
"""

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path

CLI_LAYER_BASENAMES = {"cli.py", "__main__.py"}

DOMAIN_TOKENS = [
    re.compile(r"\bZ[A-Z][A-Z_]{2,}\b"),  # Core Data column/table names
    re.compile(r"BKLibrary"),
    re.compile(r"Books\.plist"),
    re.compile(r"com\.apple"),
    re.compile(r"iBooksX"),
    re.compile(r"\bsqlite3?\b"),
    re.compile(r"Library/Containers"),
]

TEST_KNOWLEDGE_TOKENS = [
    re.compile(r"\bpytest\b"),
    re.compile(r"PYTEST_CURRENT_TEST"),
    re.compile(r"\bCliRunner\b"),
    re.compile(r"\bmonkeypatch\b"),
    re.compile(r"\bunittest\b"),
    re.compile(r"specs/"),
    re.compile(r"fixtures/users"),
    re.compile(r"\btest_reader\b"),
]

MACHINE_STATE_RE = re.compile(
    r"Path\.home\(|os\.path\.expanduser\(|expanduser\(\s*['\"]~"
    r"|environ(\.get)?\(\s*['\"]HOME['\"]"
)

MIN_MESSAGE_FRAGMENT = 12


def load_tree(repo: Path, rev: str | None) -> dict[str, str]:
    files: dict[str, str] = {}
    if rev:
        out = subprocess.run(
            ["git", "-C", str(repo), "ls-tree", "-r", "--name-only", rev],
            capture_output=True, text=True, check=True,
        ).stdout.splitlines()
        for rel in out:
            if rel.endswith(".py"):
                blob = subprocess.run(
                    ["git", "-C", str(repo), "show", f"{rev}:{rel}"],
                    capture_output=True, text=True,
                )
                if blob.returncode == 0:
                    files[rel] = blob.stdout
    else:
        for p in sorted(repo.rglob("*.py")):
            rel = str(p.relative_to(repo))
            if any(seg.startswith(".") or seg in ("__pycache__", ".venv", "venv")
                   for seg in Path(rel).parts):
                continue
            try:
                files[rel] = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
    return files


def split_tree(files, package, specs_dir):
    prod = {p: s for p, s in files.items() if p.startswith(package + "/")}
    specs = {p: s for p, s in files.items()
             if p.startswith(specs_dir + "/") or p == "conftest.py"
             or p.startswith("tests/")}
    return prod, specs


def parse_all(files):
    trees = {}
    for path, src in files.items():
        try:
            trees[path] = ast.parse(src)
        except SyntaxError:
            pass
    return trees


def module_name_of(path: str) -> str:
    return path[:-3].replace("/", ".").removesuffix(".__init__")


def from_imports(tree: ast.Module, own_module: str) -> dict[str, str]:
    """Map of name -> origin module for names this module imports."""
    imports: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            for alias in node.names:
                imports[alias.asname or alias.name] = node.module
    return imports


def defined_names(tree: ast.Module) -> set[str]:
    names = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.add(t.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    return names


def patch_targets(tree: ast.Module):
    """Yield (dotted_target, lineno) for patch()/monkeypatch.setattr() calls.

    Handles patch("a.b.name"), patch.object(obj, "name") -> ("<obj>.name"),
    monkeypatch.setattr("a.b.name", ...), monkeypatch.setattr(obj, "name", ...).
    """
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        fname = None
        if isinstance(func, ast.Name):
            fname = func.id
        elif isinstance(func, ast.Attribute):
            fname = func.attr
        if fname == "patch" or (
            fname == "object" and isinstance(func, ast.Attribute)
            and isinstance(func.value, (ast.Name, ast.Attribute))
            and getattr(func.value, "id", getattr(func.value, "attr", None)) == "patch"
        ):
            if fname == "patch" and node.args and isinstance(node.args[0], ast.Constant) \
                    and isinstance(node.args[0].value, str):
                yield node.args[0].value, node.lineno
            elif fname == "object" and len(node.args) >= 2 \
                    and isinstance(node.args[1], ast.Constant) \
                    and isinstance(node.args[1].value, str):
                base = ast.unparse(node.args[0])
                yield f"{base}.{node.args[1].value}", node.lineno
        elif fname == "setattr" and isinstance(func, ast.Attribute) \
                and getattr(func.value, "id", None) == "monkeypatch" and node.args:
            first = node.args[0]
            if isinstance(first, ast.Constant) and isinstance(first.value, str):
                yield first.value, node.lineno
            elif len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) \
                    and isinstance(node.args[1].value, str):
                base = ast.unparse(first)
                yield f"{base}.{node.args[1].value}", node.lineno


def grep_lines(src: str, regexes):
    for i, line in enumerate(src.splitlines(), 1):
        for rx in regexes:
            m = rx.search(line)
            if m:
                yield i, m.group(0)
                break


# ---------------------------------------------------------------- checks

def check_cli_domain_knowledge(prod, findings):
    """T-66: CLI-layer files must not carry library-owned domain knowledge."""
    for path, src in prod.items():
        if Path(path).name not in CLI_LAYER_BASENAMES:
            continue
        for lineno, tok in grep_lines(src, DOMAIN_TOKENS):
            findings.append(
                f"cli-owns-domain-knowledge: {path}:{lineno} CLI layer references "
                f"library-owned domain token {tok!r} (T-66)"
            )


def check_test_knowledge_in_production(prod, findings):
    """T-74: production code must not reference spec-tree identifiers."""
    for path, src in prod.items():
        for lineno, tok in grep_lines(src, TEST_KNOWLEDGE_TOKENS):
            findings.append(
                f"test-knowledge-in-production: {path}:{lineno} production code "
                f"references test-environment identifier {tok!r} (T-74)"
            )


def check_seam_patches(prod, prod_trees, spec_trees, spec_srcs, findings):
    """T-72/L-09 and the borrow/internal-identifier cases, from patch targets."""
    prod_modules = {module_name_of(p): p for p in prod}
    imports_by_module = {}
    defs_by_module = {}
    for path, tree in prod_trees.items():
        mod = module_name_of(path)
        imports_by_module[mod] = from_imports(tree, mod)
        defs_by_module[mod] = defined_names(tree)

    for spec_path, tree in spec_trees.items():
        for target, lineno in patch_targets(tree):
            mod, _, name = target.rpartition(".")
            if not name:
                continue
            if name.startswith("_") and not name.startswith("__"):
                findings.append(
                    f"private-seam-patch: {spec_path}:{lineno} spec patches private "
                    f"name {target!r} instead of the front-door seam "
                    f"(--user/user_home parameter) (T-72, L-09)"
                )
                continue
            if mod not in prod_modules:
                continue
            origin = imports_by_module.get(mod, {}).get(name)
            if origin and name.isupper():
                borrow_rx = re.compile(
                    rf"assert\s+\S*\b{name}\b\s+(is|==)\s+\S*\b{name}\b"
                )
                specified = any(borrow_rx.search(s) for s in spec_srcs.values())
                if not specified:
                    findings.append(
                        f"unspecified-borrow: {spec_path}:{lineno} spec patches "
                        f"{target!r}, a constant {mod} borrows from {origin}, but no "
                        f"spec asserts the delegation contract "
                        f"({mod}.{name} is {origin}.{name}) (T-72, L-09)"
                    )
            elif name in defs_by_module.get(mod, set()) \
                    and name not in imports_by_module.get(mod, {}):
                findings.append(
                    f"internal-identifier-patch: {spec_path}:{lineno} spec patches "
                    f"{target!r}, defined inside the module under test — asserting "
                    f"through an implementation identifier, not observable behavior "
                    f"(T-61)"
                )


def check_duplicated_vocabulary_constant(prod_trees, findings):
    """T-69: a vocabulary constant defined in two production modules."""
    sites: dict[str, list[tuple[str, int]]] = {}
    for path, tree in prod_trees.items():
        for node in tree.body:
            targets = []
            if isinstance(node, ast.Assign):
                targets = [t for t in node.targets if isinstance(t, ast.Name)]
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                targets = [node.target]
            for t in targets:
                if t.id.isupper() and len(t.id) > 1 and not t.id.startswith("__"):
                    sites.setdefault(t.id, []).append((path, node.lineno))
    for name, locs in sites.items():
        if len({p for p, _ in locs}) > 1:
            where = ", ".join(f"{p}:{ln}" for p, ln in locs)
            findings.append(
                f"duplicated-vocabulary-constant: {where} constant {name!r} is "
                f"defined in multiple production modules instead of one module "
                f"owning it and others importing it (T-69)"
            )


def check_cross_file_duplicate_spec(spec_trees, findings):
    """T-69: the same it_ spec name defined in more than one spec file."""
    sites: dict[str, list[str]] = {}
    for path, tree in spec_trees.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("it_"):
                sites.setdefault(node.name, []).append(f"{path}:{node.lineno}")
    for name, locs in sites.items():
        if len({loc.split(":")[0] for loc in locs}) > 1:
            findings.append(
                f"duplicate-spec-across-layers: {', '.join(locs)} spec {name!r} "
                f"exists in multiple files — one behavior, one owning layer (T-69)"
            )


def _raise_fragments(prod_trees):
    frags = []
    for path, tree in prod_trees.items():
        if Path(path).name in CLI_LAYER_BASENAMES:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Raise):
                continue
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str) \
                        and len(sub.value) >= MIN_MESSAGE_FRAGMENT:
                    frags.append((sub.value, path))
    return frags


def check_boundary_lower_layer_text(prod_trees, spec_trees, findings):
    """T-70/T-61: a boundary (mocking) spec asserting the lower layer's wording."""
    frags = _raise_fragments(prod_trees)
    if not frags:
        return
    for spec_path, tree in spec_trees.items():
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef) or not node.name.startswith("it_"):
                continue
            mocks = list(patch_targets(node))
            if not mocks:
                continue
            for sub in ast.walk(node):
                if not isinstance(sub, ast.Assert):
                    continue
                for c in ast.walk(sub):
                    if isinstance(c, ast.Constant) and isinstance(c.value, str) \
                            and len(c.value) >= MIN_MESSAGE_FRAGMENT:
                        for frag, frag_path in frags:
                            if c.value in frag or frag in c.value:
                                findings.append(
                                    f"lower-layer-text-in-boundary-spec: "
                                    f"{spec_path}:{c.lineno} boundary spec asserts "
                                    f"wording owned by {frag_path} — assert the "
                                    f"sentinel your double injected (T-70, T-61)"
                                )
                                break


def _subprocess_spec_locs(spec_trees):
    locs = []
    for path, tree in spec_trees.items():
        helper_names = set()
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                calls_subprocess = any(
                    isinstance(c, ast.Attribute) and isinstance(c.value, ast.Name)
                    and c.value.id == "subprocess"
                    for c in ast.walk(node)
                )
                if calls_subprocess and not node.name.startswith(("it_", "describe_")):
                    helper_names.add(node.name)
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef) or not node.name.startswith("it_"):
                continue
            uses = any(
                (isinstance(c, ast.Attribute) and isinstance(c.value, ast.Name)
                 and c.value.id == "subprocess")
                or (isinstance(c, ast.Name) and c.id in helper_names)
                for c in ast.walk(node)
            )
            if uses:
                locs.append(f"{path}:{node.lineno}")
    return locs


def check_subprocess_multiplicity(spec_trees, spec_srcs, findings):
    """T-71: with an in-process seam available, keep exactly one subprocess spec."""
    in_process_seam = any("CliRunner" in s for s in spec_srcs.values())
    if not in_process_seam:
        return
    locs = _subprocess_spec_locs(spec_trees)
    if len(locs) > 1:
        findings.append(
            f"multiple-subprocess-entrypoint-specs: {len(locs)} subprocess-driven "
            f"specs while an in-process seam (CliRunner) exists — one wiring spec "
            f"proves the entry point, the rest re-test behavior slowly: "
            f"{', '.join(locs)} (T-71)"
        )


def check_machine_state(spec_srcs, findings):
    """T-67: a spec reading real machine state is an integration test."""
    for path, src in spec_srcs.items():
        lowered = path.lower()
        if "integration" in lowered or "e2e" in lowered:
            continue
        for i, line in enumerate(src.splitlines(), 1):
            if MACHINE_STATE_RE.search(line):
                findings.append(
                    f"machine-state-in-unit-spec: {path}:{i} spec reads real "
                    f"machine state ({MACHINE_STATE_RE.search(line).group(0)!r}) "
                    f"outside an integration-labeled file (T-67)"
                )


def check_absolute_path_literal(spec_trees, findings):
    """T-61: absolute machine-path literals asserted in acceptance-layer specs."""
    for path, tree in spec_trees.items():
        lowered = path.lower()
        name = Path(path).name
        is_acceptance = (
            "acceptance" in lowered or "e2e" in lowered or name.startswith("cli")
        )
        if not is_acceptance:
            continue
        joined_parts = {
            id(v) for node in ast.walk(tree) if isinstance(node, ast.JoinedStr)
            for v in ast.walk(node)
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                    and id(node) not in joined_parts \
                    and (node.value.startswith("/Users/")
                         or node.value.startswith("/home/")):
                findings.append(
                    f"absolute-machine-path-in-spec: {path}:{node.lineno} "
                    f"acceptance-layer spec pins absolute machine path "
                    f"{node.value!r} (T-61)"
                )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=".", help="repo root (tree to scan)")
    ap.add_argument("--rev", default=None, help="git revision instead of working tree")
    ap.add_argument("--package", default="bookminder", help="production package dir")
    ap.add_argument("--specs", default="specs", help="spec tree dir")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    files = load_tree(repo, args.rev)
    prod, specs = split_tree(files, args.package, args.specs)
    prod_trees = parse_all(prod)
    spec_trees = parse_all(specs)

    findings: list[str] = []
    check_cli_domain_knowledge(prod, findings)
    check_test_knowledge_in_production(prod, findings)
    check_seam_patches(prod, prod_trees, spec_trees, specs, findings)
    check_duplicated_vocabulary_constant(prod_trees, findings)
    check_cross_file_duplicate_spec(spec_trees, findings)
    check_boundary_lower_layer_text(prod_trees, spec_trees, findings)
    check_subprocess_multiplicity(spec_trees, specs, findings)
    check_machine_state(specs, findings)
    check_absolute_path_literal(spec_trees, findings)

    for f in findings:
        print(f)
    if not findings:
        print("f4_layering: clean", file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
