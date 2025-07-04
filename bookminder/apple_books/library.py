"""Apple Books library access functions."""

import datetime
import plistlib
import sqlite3
from pathlib import Path
from typing import Any, NotRequired, TypedDict

from bookminder import BookminderError

APPLE_EPOCH = datetime.datetime(2001, 1, 1, tzinfo=datetime.UTC)
APPLE_CONTAINERS = "Library/Containers/com.apple"


def _books_plist(user_home: Path) -> Path:
    return (
        user_home
        / f"{APPLE_CONTAINERS}.BKAgentService/Data/Documents/iBooks/Books/Books.plist"
    )


def _get_bklibrary_db_file(user_home: Path) -> Path:
    bklibrary_path = user_home / f"{APPLE_CONTAINERS}.iBooksX/Data/Documents/BKLibrary"
    if not bklibrary_path.exists():
        raise BookminderError(
            f"BKLibrary directory not found: {bklibrary_path}. "
            "Apple Books database not found."
        )

    db_files = list(bklibrary_path.glob("BKLibrary-*.sqlite"))
    if not db_files:
        raise BookminderError(
            f"No BKLibrary database found in: {bklibrary_path}. "
            "Apple Books database not found."
        )

    return db_files[0]


class Book(TypedDict):
    """Book metadata from Apple Books library."""

    title: str
    path: str
    author: str
    updated: datetime.datetime
    reading_progress_percentage: NotRequired[int]
    is_cloud: NotRequired[bool]


def _apple_timestamp_to_datetime(timestamp: float) -> datetime.datetime:
    return APPLE_EPOCH + datetime.timedelta(seconds=timestamp)


def _row_to_book(row: sqlite3.Row) -> Book:
    return Book(
        title=row["ZTITLE"] or "Unknown",
        author=row["ZAUTHOR"] or "Unknown",
        path="",  # Path requires Books.plist correlation with ZASSETID
        updated=_apple_timestamp_to_datetime(row["ZLASTOPENDATE"]),
        reading_progress_percentage=int(row["ZREADINGPROGRESS"] * 100),
        is_cloud=row["ZSTATE"] == 3,
    )


def _read_books_plist(user_home: Path) -> list[dict[str, Any]]:
    books_plist = _books_plist(user_home)
    if not books_plist.exists():
        raise BookminderError(
            f"Books.plist not found: {books_plist}. "
            "Apple Books not found. Has it been opened on this account?"
        )

    with open(books_plist, "rb") as f:
        plist_data = plistlib.load(f)
    books = plist_data.get("Books", [])
    return books if isinstance(books, list) else []


def list_books(user_home: Path) -> list[Book]:
    """List books from the Apple Books library."""
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


def find_book_by_title(title: str, user_home: Path) -> Book | None:
    """Find a book by exact title match."""
    return next(
        (book for book in list_books(user_home) if book["title"] == title), None
    )


def list_recent_books(user_home: Path, filter: str | None = None) -> list[Book]:
    """List recently read books with progress from BKLibrary database."""
    try:
        _books_plist(user_home)  # Call to trigger FileNotFoundError if plist is missing

        db_file = _get_bklibrary_db_file(user_home)

        with sqlite3.connect(db_file) as conn:
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()

            query = """
                SELECT ZTITLE, ZAUTHOR, ZREADINGPROGRESS, ZLASTOPENDATE, ZSTATE
                FROM ZBKLIBRARYASSET
                WHERE ZREADINGPROGRESS > 0
            """

            params = []
            if filter == "cloud":
                query += " AND ZSTATE = ?"
                params.append(3)

            query += " ORDER BY ZLASTOPENDATE DESC LIMIT 10"

            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()

            books = [_row_to_book(row) for row in rows]

            return books
    except FileNotFoundError as e:
        raise BookminderError(f"Error accessing Apple Books files: {e}") from e
    except sqlite3.Error as e:
        raise BookminderError(f"Error reading Apple Books database: {e}") from e
