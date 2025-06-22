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


class Book(TypedDict):
    """Book metadata from Apple Books library."""

    title: str
    path: str
    author: str
    updated: datetime.datetime
    progress: NotRequired[float]  # Reading progress as percentage (0.0-100.0)


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
    # Find BKLibrary database using glob pattern
    home = Path.home()
    db_pattern = str(
        home
        / "Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary"
        / "BKLibrary-*.sqlite"
    )
    db_files = glob.glob(db_pattern)

    if not db_files:
        # No database found - return empty list for now
        return []

    db_path = db_files[0]  # Use first match

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()

            # Query from docs/apple_books.md
            query = """
                SELECT ZTITLE, ZAUTHOR, ZREADINGPROGRESS * 100 as progress,
                       ZLASTOPENDATE
                FROM ZBKLIBRARYASSET
                WHERE ZREADINGPROGRESS > 0
                ORDER BY ZLASTOPENDATE DESC
                LIMIT 10
            """

            cursor.execute(query)
            rows = cursor.fetchall()

            books = []
            for row in rows:
                # Convert Apple timestamp (Core Data format) to datetime
                apple_epoch = datetime.datetime(2001, 1, 1, tzinfo=datetime.UTC)
                last_opened = apple_epoch + datetime.timedelta(
                    seconds=row["ZLASTOPENDATE"] or 0
                )

                book = Book(
                    title=row["ZTITLE"] or "Unknown",
                    author=row["ZAUTHOR"] or "Unknown",
                    path="",  # We don't need path for recent books display
                    updated=last_opened,
                    progress=float(row["progress"] or 0),
                )
                books.append(book)

            return books

    except sqlite3.Error:
        # Database error (locked, corrupted, etc.) - return empty list
        return []
