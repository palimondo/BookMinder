"""Apple Books library access functions."""

import datetime
import plistlib
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NotRequired, TypedDict

APPLE_EPOCH = datetime.datetime(2001, 1, 1, tzinfo=datetime.UTC)


@dataclass
class LibraryPaths:
    """Encapsulates all Apple Books library paths for a user."""

    home: Path

    @classmethod
    def for_user(cls, user_name: str | None = None) -> "LibraryPaths":  # noqa: D102
        if not user_name:
            return cls(Path.home())

        user_path = Path(user_name)
        if user_path.is_absolute():
            return cls(user_path)
        else:
            return cls(Path(f"/Users/{user_name}"))

    @property
    def books_container(self) -> Path:  # noqa: D102
        return (
            self.home
            / "Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books"
        )

    @property
    def books_plist(self) -> Path:  # noqa: D102
        return self.books_container / "Books.plist"

    @property
    def bklibrary_dir(self) -> Path:  # noqa: D102
        return (
            self.home / "Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary"
        )

    @property
    def bklibrary_db(self) -> Path:  # noqa: D102
        if not self.bklibrary_dir.exists():
            raise FileNotFoundError(
                f"BKLibrary directory not found: {self.bklibrary_dir}"
            )

        db_files = list(self.bklibrary_dir.glob("BKLibrary-*.sqlite"))
        if not db_files:
            raise FileNotFoundError(
                f"No BKLibrary database found in: {self.bklibrary_dir}"
            )

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


def _read_books_plist(paths: LibraryPaths) -> list[dict[str, Any]]:
    if not paths.books_plist.exists():
        raise FileNotFoundError(f"Books.plist not found: {paths.books_plist}")

    with open(paths.books_plist, "rb") as f:
        plist_data = plistlib.load(f)
    books = plist_data.get("Books", [])
    return books if isinstance(books, list) else []


def list_books(user_name: str | None = None) -> list[Book]:
    """List books from the Apple Books library."""
    paths = LibraryPaths.for_user(user_name)
    raw_books = _read_books_plist(paths)

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
    paths = LibraryPaths.for_user(user_name)

    # Check if BKAgentService exists (Apple Books opened)
    if not paths.books_plist.exists():
        raise FileNotFoundError("BKAgentService container not found")

    try:
        db_file = paths.bklibrary_db
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
