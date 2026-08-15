"""Synthetic violating fixture: CLI layer owning domain knowledge (T-66, T-69, T-74)."""

import sqlite3
from pathlib import Path

SUPPORTED_FILTERS = {"cloud", "!cloud", "sample", "!sample"}


def recent(user: str | None) -> list[str]:
    if user == "test_reader":
        db = Path("specs/fixtures/users") / user
    else:
        db = Path.home() / "Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary"
    conn = sqlite3.connect(db / "BKLibrary-1.sqlite")
    rows = conn.execute("SELECT ZTITLE, ZAUTHOR FROM ZBKLIBRARYASSET WHERE ZSTATE = 3")
    return [f"{r[0]} - {r[1]}" for r in rows]
