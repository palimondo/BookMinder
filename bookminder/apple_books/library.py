"""Apple Books library access functions."""

import datetime
import glob
import plistlib
import sqlite3
from pathlib import Path
from typing import Any, NotRequired, TypedDict

BOOKS_PATH = (
    Path.home()
    / "Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books"
)
BOOKS_PLIST = BOOKS_PATH / "Books.plist"

BKLIBRARY_PATH = (
    Path.home() / "Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary"
)
_db_files = glob.glob(str(BKLIBRARY_PATH / "BKLibrary-*.sqlite"))
BKLIBRARY_DB_FILE = Path(_db_files[0]) if _db_files else None


class Book(TypedDict):
    """Book metadata from Apple Books library."""

    title: str
    path: str
    author: str
    updated: datetime.datetime
    reading_progress_percentage: NotRequired[int]


def _apple_timestamp_to_datetime(timestamp: float | None) -> datetime.datetime:
    """Convert Apple Core Data timestamp to Python datetime.

    Apple uses January 1, 2001 as epoch (vs Unix epoch of January 1, 1970).
    """
    if timestamp is None:
        return datetime.datetime.min

    apple_epoch = datetime.datetime(2001, 1, 1, tzinfo=datetime.UTC)
    return apple_epoch + datetime.timedelta(seconds=timestamp)


def _row_to_book(row: sqlite3.Row) -> Book:
    """Convert database row to Book object."""
    return Book(
        title=row["ZTITLE"] or "Unknown",
        author=row["ZAUTHOR"] or "Unknown",
        path="",  # TODO: Path not in BKLibrary DB - need Books.plist correlation
        updated=_apple_timestamp_to_datetime(row["ZLASTOPENDATE"]),
        reading_progress_percentage=int(row["ZREADINGPROGRESS"] * 100),
    )


def _read_books_plist() -> list[dict[str, Any]]:
    with open(BOOKS_PLIST, "rb") as f:
        plist_data = plistlib.load(f)
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


def list_recent_books() -> list[Book]:
    """List recently read books with progress from BKLibrary database."""
    if not BKLIBRARY_DB_FILE:
        return []

    try:
        with sqlite3.connect(BKLIBRARY_DB_FILE) as conn:
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()

            query = """
                SELECT ZTITLE, ZAUTHOR, ZREADINGPROGRESS, ZLASTOPENDATE
                FROM ZBKLIBRARYASSET
                WHERE ZREADINGPROGRESS > 0
                ORDER BY ZLASTOPENDATE DESC
                LIMIT 10
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            books = [_row_to_book(row) for row in rows]

            return books

    except sqlite3.Error:
        # TODO: Handle specific errors - database locked, missing table, etc.
        return []
