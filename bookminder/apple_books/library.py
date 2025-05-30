"""Apple Books library access functions."""

import datetime
import plistlib
import subprocess
from pathlib import Path
from typing import Any, TypedDict

BOOKS_PATH = (
    Path.home()
    / "Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books"
)
BOOKS_PLIST = BOOKS_PATH / "Books.plist"


class Book(TypedDict):
    """Book metadata from Apple Books library."""

    title: str
    path: str
    author: str
    updated: datetime.datetime


def _read_books_plist() -> list[dict[str, Any]]:
    # Use plutil to convert binary plist to XML format which plistlib can read
    result = subprocess.run(
        ["plutil", "-convert", "xml1", "-o", "-", str(BOOKS_PLIST)],
        capture_output=True,
        text=False,
        check=True,
    )

    plist_data = plistlib.loads(result.stdout)
    books = plist_data.get("Books", [])
    return books if isinstance(books, list) else []


def list_books() -> list[Book]:
    """List books from the Apple Books library."""
    raw_books = _read_books_plist()

    books: list[Book] = [
        Book(
            title=book.get("itemName", "Unknown"),
            path=book.get("path", ""),
            author=book.get("artistName", "Unknown"),
            updated=book.get("updateDate", datetime.datetime.min),
        )
        for book in raw_books
    ]
    return books


def find_book_by_title(title: str) -> Book | None:
    """Find a book by exact title match."""
    return next((book for book in list_books() if book["title"] == title), None)
