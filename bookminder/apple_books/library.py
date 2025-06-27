"""Apple Books library access functions."""

import datetime
import plistlib
import sqlite3
from pathlib import Path
from typing import Any, NotRequired, TypedDict

APPLE_EPOCH = datetime.datetime(2001, 1, 1, tzinfo=datetime.UTC)
APPLE_CONTAINERS = "Library/Containers/com.apple"


def _get_books_path(user_home: Path) -> Path:
    return user_home / f"{APPLE_CONTAINERS}.BKAgentService/Data/Documents/iBooks/Books"


def _get_bklibrary_db_file(user_home: Path) -> Path:
    bklibrary_path = user_home / f"{APPLE_CONTAINERS}.iBooksX/Data/Documents/BKLibrary"
    if not bklibrary_path.exists():
        raise FileNotFoundError(f"BKLibrary directory not found: {bklibrary_path}")

    db_files = list(bklibrary_path.glob("BKLibrary-*.sqlite"))
    if not db_files:
        raise FileNotFoundError(f"No BKLibrary database found in: {bklibrary_path}")

    return db_files[0]


class Book(TypedDict):
    """Book metadata from Apple Books library."""

    title: str
    path: str
    author: str
    updated: datetime.datetime
    reading_progress_percentage: NotRequired[int]


def _apple_timestamp_to_datetime(timestamp: float) -> datetime.datetime:
    return APPLE_EPOCH + datetime.timedelta(seconds=timestamp)


def _row_to_book(row: sqlite3.Row) -> Book:
    return Book(
        title=row["ZTITLE"] or "Unknown",
        author=row["ZAUTHOR"] or "Unknown",
        path="",  # Path requires Books.plist correlation with ZASSETID
        updated=_apple_timestamp_to_datetime(row["ZLASTOPENDATE"]),
        reading_progress_percentage=int(row["ZREADINGPROGRESS"] * 100),
    )


def _read_books_plist(user_home: Path) -> list[dict[str, Any]]:
    books_plist = _get_books_path(user_home) / "Books.plist"
    if not books_plist.exists():
        raise FileNotFoundError(f"Books.plist not found: {books_plist}")

    with open(books_plist, "rb") as f:
        plist_data = plistlib.load(f)
    books = plist_data.get("Books", [])
    return books if isinstance(books, list) else []


def list_books(user_home: Path | None = None) -> list[Book]:
    """List books from the Apple Books library."""
    if user_home is None:
        user_home = Path.home()
    raw_books = _read_books_plist(user_home)

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


def find_book_by_title(title: str, user_home: Path | None = None) -> Book | None:
    """Find a book by exact title match."""
    return next(
        (book for book in list_books(user_home) if book["title"] == title), None
    )


def list_recent_books(user_home: Path | None = None) -> list[Book]:
    """List recently read books with progress from BKLibrary database."""
    if user_home is None:
        user_home = Path.home()

    # Check if BKAgentService exists (Apple Books opened)
    books_plist = _get_books_path(user_home) / "Books.plist"
    if not books_plist.exists():
        raise FileNotFoundError("BKAgentService container not found")

    try:
        db_file = _get_bklibrary_db_file(user_home)
    except FileNotFoundError:
        # Database doesn't exist - either legacy installation or never added books
        raise

    with sqlite3.connect(db_file) as conn:
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
