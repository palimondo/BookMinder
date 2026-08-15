#!/usr/bin/env python3
"""SYNTHETIC negative fixture for the F6 refactor-honesty detector.

Builds a throwaway git repo whose refactor-labeled commits each embody one
named failure mode, plus one honest refactor commit that must stay clean.
Usage: python3 make_fixture_repo.py /path/to/target-dir
"""

import subprocess
import sys
from pathlib import Path

CALC_V1 = '''\
def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ValueError("division by zero")
    return a / b
'''

SPEC_V1 = '''\
import pytest

from calc import add, divide


def describe_add():
    def it_adds_two_numbers():
        assert add(2, 3) == 5


def describe_divide():
    def it_divides():
        assert divide(6, 3) == 2

    def it_rejects_zero_divisor():
        with pytest.raises(ValueError):
            divide(1, 0)
        assert add(0, 0) == 0
'''

# refactor: behavior change (add now off by one) -> refactor-behavior-broken
CALC_V2 = CALC_V1.replace("return a + b", "return a + b + 1")

# refactor: honest cleanup -> must stay clean
CALC_V3 = CALC_V2.replace(
    "def divide(a, b):",
    "def divide(a, b):\n    _check(b)",
).replace(
    "    if b == 0:\n        raise ValueError(\"division by zero\")\n    return a / b",
    "    return a / b\n\n\ndef _check(b):\n    if b == 0:\n        raise ValueError(\"division by zero\")",
)

# refactor: new public function with novel body + new branch
# -> impl-public-addition, impl-branch-addition
CALC_V4 = CALC_V3 + '''\


def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x
'''

# refactor: rename divide -> div but leave a stale reference -> rename-residue
CALC_V5 = CALC_V4.replace("def divide(a, b):", "def div(a, b):")
UTIL_V5 = '''\
from calc import add


def half(a):
    """Uses divide from calc."""
    return divide(a, 2)
'''

# refactor: rewrite spec expectation under the label -> spec-expectation-changed
SPEC_V6 = SPEC_V1.replace("assert add(2, 3) == 5", "assert add(2, 3) == 6")


def run(cwd: Path, *args: str) -> None:
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


def commit(repo: Path, msg: str, files: dict[str, str]) -> None:
    for name, content in files.items():
        (repo / name).write_text(content)
    run(repo, "git", "add", "-A")
    run(repo, "git", "commit", "-q", "-m", msg)


def main() -> None:
    repo = Path(sys.argv[1])
    repo.mkdir(parents=True, exist_ok=True)
    run(repo, "git", "init", "-q")
    run(repo, "git", "config", "user.email", "fixture@example.com")
    run(repo, "git", "config", "user.name", "F6 Fixture")

    commit(repo, "feat: calculator with specs",
           {"calc.py": CALC_V1, "calc_spec.py": SPEC_V1})
    commit(repo, "refactor: simplify addition", {"calc.py": CALC_V2})
    commit(repo, "refactor: extract divisor guard", {"calc.py": CALC_V3})
    commit(repo, "refactor: tidy calc module", {"calc.py": CALC_V4})
    commit(repo, "refactor: rename divide to div",
           {"calc.py": CALC_V5, "util.py": UTIL_V5})
    commit(repo, "refactor: clean up spec style", {"calc_spec.py": SPEC_V6})
    print(f"fixture repo at {repo}")


if __name__ == "__main__":
    main()
