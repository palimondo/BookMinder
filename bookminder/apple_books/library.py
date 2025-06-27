"""Apple Books library access functions."""

import datetime
import plistlib
import sqlite3
from pathlib import Path
from typing import Any, NotRequired, TypedDict

APPLE_EPOCH = datetime.datetime(2001, 1, 1, tzinfo=datetime.UTC)


def _get_user_home(user_name: str | None = None) -> Path:
    if not user_name:
        return Path.home()

    user_path = Path(user_name)
    if user_path.is_absolute():
        return user_path
    else:
        return Path(f"/Users/{user_name}")


def _get_books_path(user_name: str | None = None) -> Path:
    home = _get_user_home(user_name)
    return (
        home / "Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books"
    )


def _get_books_plist(user_name: str | None = None) -> Path:
    return _get_books_path(user_name) / "Books.plist"


def _get_bklibrary_path(user_name: str | None = None) -> Path:
    home = _get_user_home(user_name)
    return home / "Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary"


def _get_bklibrary_db_file(user_name: str | None = None) -> Path:
    bklibrary_path = _get_bklibrary_path(user_name)
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


def _read_books_plist(user_name: str | None = None) -> list[dict[str, Any]]:
    books_plist = _get_books_plist(user_name)
    if not books_plist.exists():
        raise FileNotFoundError(f"Books.plist not found: {books_plist}")

    with open(books_plist, "rb") as f:
        plist_data = plistlib.load(f)
    books = plist_data.get("Books", [])
    return books if isinstance(books, list) else []


def list_books(user_name: str | None = None) -> list[Book]:
    """List books from the Apple Books library."""
    raw_books = _read_books_plist(user_name)

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


def find_book_by_title(title: str, user_name: str | None = None) -> Book | None:
    """Find a book by exact title match."""
    return next(
        (book for book in list_books(user_name) if book["title"] == title), None
    )


def list_recent_books(user_name: str | None = None) -> list[Book]:
    """List recently read books with progress from BKLibrary database."""
    # Check if BKAgentService exists (Apple Books opened)
    try:
        books_plist = _get_books_plist(user_name)
        if not books_plist.exists():
            raise FileNotFoundError("BKAgentService container not found")
    except FileNotFoundError:
        raise FileNotFoundError("BKAgentService container not found") from None

    try:
        db_file = _get_bklibrary_db_file(user_name)
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
