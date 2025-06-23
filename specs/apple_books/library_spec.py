from pathlib import Path

import pytest

from bookminder.apple_books.library import (
    find_book_by_title,
    list_books,
    list_recent_books,
)


@pytest.fixture(autouse=True)
def use_test_books(monkeypatch):
    """Use test fixtures instead of real Apple Books library."""
    fixtures_path = Path(__file__).parent / "fixtures"
    test_plist = fixtures_path / "Books.plist"

    # Patch the constants to use test fixtures
    monkeypatch.setattr("bookminder.apple_books.library.BOOKS_PATH", fixtures_path)
    monkeypatch.setattr("bookminder.apple_books.library.BOOKS_PLIST", test_plist)


def describe_list_books():
    def it_finds_books_from_apple_books_directory():
        books = list_books()
        assert len(books) > 0, "Expected to find at least one book"

    def it_includes_basic_metadata_for_each_book():
        books = list_books()
        for book in books:
            assert "title" in book, f"Book missing title: {book}"
            assert "path" in book, f"Book missing path: {book}"
            assert "author" in book, f"Book missing author: {book}"
            assert "updated" in book, f"Book missing updated date: {book}"


def describe_find_book_by_title():
    def it_finds_book_by_exact_title():
        book = find_book_by_title("Growing Object-Oriented Software, Guided by Tests")
        assert book is not None, "Test book not found"
        assert "401429854.epub" in book["path"], "Found incorrect book"

    def it_returns_none_when_book_not_found():
        book = find_book_by_title("Non-existent Book Title")
        assert book is None, "Expected None for non-existent book"


def describe_list_recent_books():
    def it_returns_books_with_reading_progress():
        books = list_recent_books()
        assert len(books) > 0, "Expected to find recent books"

        for book in books:
            assert "title" in book, f"Book missing title: {book}"
            assert "author" in book, f"Book missing author: {book}"
            assert (
                "reading_progress_percentage" in book
            ), f"Book missing reading_progress_percentage: {book}"

    def it_attempts_to_read_from_bklibrary_database():
        """Test that function tries to query real database, not hardcoded data."""
        books = list_recent_books()
        # This test will fail with hardcoded data since we expect
        # actual database results (could be 0 books if no database found)
        # The key is that it should attempt database access, not return
        # exactly the 3 hardcoded books we currently have
        hardcoded_titles = {
            "The Pragmatic Programmer",
            "Continuous Delivery",
            "Test Driven Development",
        }
        actual_titles = {book["title"] for book in books}
        assert (
            actual_titles != hardcoded_titles
        ), "Function appears to return hardcoded data instead of querying database"

    def it_returns_empty_list_when_database_not_found(monkeypatch):
        """When Apple Books database is missing, should return empty list gracefully."""
        monkeypatch.setattr("bookminder.apple_books.library.BKLIBRARY_DB_FILE", None)
        books = list_recent_books()
        assert books == []

    def it_returns_empty_list_on_database_error(monkeypatch):
        """When database is corrupted or locked, should handle error gracefully."""
        # Point to a file that exists but isn't a valid SQLite database
        monkeypatch.setattr(
            "bookminder.apple_books.library.BKLIBRARY_DB_FILE", Path("/dev/null")
        )
        books = list_recent_books()
        assert books == []
