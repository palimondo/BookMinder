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

    from bookminder.apple_books.library import LibraryPaths

    # Create a test subclass that overrides the properties
    class TestLibraryPaths(LibraryPaths):
        @property
        def books_container(self):
            return fixtures_path

        @property
        def books_plist(self):
            return fixtures_path / "Books.plist"

        @property
        def bklibrary_dir(self):
            return fixtures_path  # Not used in these tests

    # Mock the for_user factory to return our test instance
    def mock_for_user(cls, user_name=None):
        return TestLibraryPaths(fixtures_path.parent.parent)

    monkeypatch.setattr(
        "bookminder.apple_books.library.LibraryPaths.for_user",
        classmethod(mock_for_user),
    )


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
    @pytest.mark.skip(reason="Need to update fixture to include database")
    def it_returns_books_with_reading_progress():
        books = list_recent_books()
        assert len(books) > 0, "Expected to find recent books"

        for book in books:
            assert "title" in book, f"Book missing title: {book}"
            assert "author" in book, f"Book missing author: {book}"
            assert (
                "reading_progress_percentage" in book
            ), f"Book missing reading_progress_percentage: {book}"
