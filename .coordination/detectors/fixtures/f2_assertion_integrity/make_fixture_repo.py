#!/usr/bin/env python3
"""SYNTHETIC fixture for the F2 assertion-integrity detector.

Builds a two-commit git repo at the given path: commit 1 holds a strong spec
suite, commit 2 weakens it in every failure mode the detector names that real
BookMinder history does not exercise. Prints the two SHAs on stdout as
BASE..WEAK for use with --range.
"""

import subprocess
import sys
from pathlib import Path

V1 = '''\
from unittest.mock import patch

from widgets import get_titles, load_items, load_rows, render, run, status
from widgets import list_books, filter_books


def describe_widgets():
    def it_lists_titles():
        titles = get_titles()
        assert len(titles) > 0
        assert titles == ["A", "B", "C"]

    def it_reports_status():
        assert status() == "fully ready"

    def it_counts_items():
        items = load_items()
        assert items == ["x", "y"]

    def it_formats_output():
        out = render()
        assert out == "A - 10%"
        assert "%" in out

    def it_handles_missing_dir():
        result = run()
        assert result == 0

    def it_reads_config():
        out = render()
        assert out == "A - 10%"
'''

V2 = '''\
import pytest
from unittest.mock import patch

from widgets import get_titles, load_items, load_rows, render, run, status
from widgets import list_books, filter_books


def describe_widgets():
    def it_lists_titles():
        titles = get_titles()
        assert len(titles) > 0
        assert "A" in titles

    def it_reports_status():
        assert status() == "partly done"

    def it_counts_items():
        items = load_items()
        assert len(items) >= 1

    def it_formats_output():
        out = render()
        assert "%" in out

    @pytest.mark.skip(reason="flaky after refactor")
    def it_handles_missing_dir():
        result = run()
        assert result == 0

    def it_reads_config():
        out = render()
        assert out == "A - 10%" or out == ""

    def it_echoes_the_mock():
        books = ["b1", "b2"]
        with patch("widgets.load_items") as m:
            m.return_value = books
            result = list_books()
        assert result == books

    def it_limits_to_recent_rows():
        rows = load_rows()
        assert len(rows) == 5

    def it_shows_reading_progress():
        result = filter_books("progress")
        assert result == []

    @pytest.mark.skip(reason="pending")
    def it_syncs_to_cloud():
        assert run() == 0
'''

WIDGETS_V1 = "def get_titles():\n    return ['A', 'B', 'C']\n"
WIDGETS_V2 = WIDGETS_V1 + "\n\ndef sync():\n    return 0\n"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True,
        check=True,
    ).stdout.strip()


def main() -> None:
    repo = Path(sys.argv[1])
    repo.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    git(repo, "config", "user.email", "fixture@example.com")
    git(repo, "config", "user.name", "F2 Fixture")

    (repo / "widgets.py").write_text(WIDGETS_V1)
    (repo / "widgets_spec.py").write_text(V1)
    git(repo, "add", "widgets.py", "widgets_spec.py")
    git(repo, "commit", "-q", "-m", "strong baseline suite")
    base = git(repo, "rev-parse", "HEAD")

    (repo / "widgets.py").write_text(WIDGETS_V2)
    (repo / "widgets_spec.py").write_text(V2)
    git(repo, "add", "widgets.py", "widgets_spec.py")
    git(repo, "commit", "-q", "-m", "refactor: tidy specs (weakens everything)")
    weak = git(repo, "rev-parse", "HEAD")

    print(f"{base}..{weak}")


if __name__ == "__main__":
    main()
