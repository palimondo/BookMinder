"""Apple Books library access functions."""

import datetime
import plistlib
import sqlite3
from pathlib import Path
from typing import Any, NotRequired, TypedDict

from bookminder import BookminderError

APPLE_EPOCH = datetime.datetime(2001, 1, 1, tzinfo=datetime.UTC)
APPLE_CONTAINERS = "Library/Containers/com.apple"

SUPPORTED_FILTERS = {"cloud", "!cloud", "sample", "!sample"}


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
    author: str
    path: NotRequired[str]
    updated: NotRequired[datetime.datetime]
    reading_progress_percentage: NotRequired[int]
    is_cloud: NotRequired[bool]
    is_sample: NotRequired[bool]


def _get_user_path(user: str | None) -> Path:
    """Convert user parameter to Path."""
    if user:
        user_path = Path(user)
        if not user_path.is_absolute():
            user_path = Path(f"/Users/{user}")
    else:
        user_path = Path.home()
    return user_path


def _apple_timestamp_to_datetime(timestamp: float) -> datetime.datetime:
    return APPLE_EPOCH + datetime.timedelta(seconds=timestamp)


def _row_to_book(row: sqlite3.Row) -> Book:
    return Book(
        title=row["ZTITLE"] or "Unknown",
        author=row["ZAUTHOR"] or "Unknown",
        path="",  # Path requires Books.plist correlation with ZASSETID
        updated=_apple_timestamp_to_datetime(row["ZLASTOPENDATE"]),
        reading_progress_percentage=int(row["ZREADINGPROGRESS"] * 100),
        is_cloud=row["ZSTATE"] in (3, 6),
        is_sample=row["ZSTATE"] == 6 or row["ZISSAMPLE"] == 1,
    )


def _read_books_plist(user_home: Path) -> list[dict[str, Any]]:
    books_plist = _books_plist(user_home)
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


def _build_books_query(where_clause: str = "", limit: int | None = None) -> str:
    """Build SQL query for fetching books from BKLibrary database."""
    query = f"""
        SELECT ZTITLE, ZAUTHOR, ZREADINGPROGRESS, ZLASTOPENDATE, ZSTATE, ZISSAMPLE
        FROM ZBKLIBRARYASSET
        {where_clause}
        ORDER BY ZLASTOPENDATE DESC
    """

    if limit:
        query += f" LIMIT {limit}"

    return query


def _query_books(
    user_home: Path,
    where_clause: str = "",
    params: tuple = (),
    limit: int | None = None,
) -> list[Book]:
    """Query books from BKLibrary database with optional WHERE clause."""
    db_file = _get_bklibrary_db_file(user_home)

    with sqlite3.connect(db_file) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = _build_books_query(where_clause, limit)
        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [_row_to_book(row) for row in rows]


def list_recent_books(user: str | None = None, filter: str | None = None) -> list[Book]:
    """List recently read books with progress from BKLibrary database."""
    user_home = _get_user_path(user)
    try:
        where_parts = ["WHERE ZREADINGPROGRESS > 0"]
        params = []

        if filter == "cloud":
            where_parts.append("AND ZSTATE = ?")
            params.append(3)
        elif filter == "!cloud":
            where_parts.append("AND ZSTATE != ?")
            params.append(3)

        where_clause = " ".join(where_parts)
        return _query_books(user_home, where_clause, tuple(params), limit=10)
    except sqlite3.Error as e:
        raise BookminderError(f"Error reading Apple Books database: {e}") from e


def list_all_books(user: str | None = None, filter: str | None = None) -> list[Book]:
    """List all books from BKLibrary database."""
    user_home = _get_user_path(user)

    where_clause = ""
    if filter == "sample":
        where_clause = "WHERE (ZSTATE = 6 OR ZISSAMPLE = 1)"
    elif filter == "!sample":
        where_clause = "WHERE ZSTATE != 6 AND (ZISSAMPLE != 1 OR ZISSAMPLE IS NULL)"

    return _query_books(user_home, where_clause)
