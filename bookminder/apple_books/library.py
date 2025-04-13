"""Apple Books library access functions."""

import os
import subprocess
import plistlib
import datetime
from typing import List, Dict, Any, Optional


# Path to Apple Books library
BOOKS_PATH = os.path.expanduser(
    "~/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books"
)
BOOKS_PLIST = os.path.join(BOOKS_PATH, "Books.plist")


def _read_books_plist() -> List[Dict[str, Any]]:
    """
    Read the Books.plist file and extract book data.

    Returns:
        List of book dictionaries from the plist file
    """
    # Use plutil to convert binary plist to XML format which plistlib can read
    result = subprocess.run(
        ["plutil", "-convert", "xml1", "-o", "-", BOOKS_PLIST],
        capture_output=True,
        text=False,
        check=True,
    )

    # Parse the XML plist data
    plist_data = plistlib.loads(result.stdout)
    return plist_data.get("Books", [])


def list_books(sort_by: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List books from the Apple Books library.

    Args:
        sort_by: Optional field to sort by, e.g. 'updated'

    Returns:
        List of book dictionaries with metadata
    """
    try:
        raw_books = _read_books_plist()

        # Convert to our standardized format
        books = []
        for book in raw_books:
            # Skip books that don't have paths or don't exist
            path = book.get("path")
            if not path or not os.path.exists(path):
                continue

            # Create standardized book entry
            book_entry = {
                "title": book.get("itemName", "Unknown"),
                "path": path,
                "author": book.get("artistName", "Unknown"),
                "updated": book.get("updateDate", datetime.datetime.min),
            }
            books.append(book_entry)

        # Sort books if requested
        if sort_by == "updated" and books:
            books.sort(key=lambda b: b["updated"], reverse=True)

        return books
    except Exception as e:
        print(f"Error reading books: {e}")
        return []


def find_book_by_title(title: str) -> Optional[Dict[str, Any]]:
    """
    Find a book by its title.

    Args:
        title: The title to search for

    Returns:
        Book dictionary if found, None otherwise
    """
    books = list_books()
    for book in books:
        if book["title"] == title:
            return book
    return None
