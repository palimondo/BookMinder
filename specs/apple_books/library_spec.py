from pathlib import Path

from bookminder.apple_books.library import (
    find_book_by_title,
    list_books,
    list_recent_books,
)

# Path to test home directory with proper Apple structure
TEST_HOME = Path(__file__).parent / "fixtures/users/test_reader"


def describe_list_books():
    def it_finds_books_from_apple_books_directory():
        books = list_books(TEST_HOME)
        assert len(books) > 0, "Expected to find at least one book"

    def it_includes_basic_metadata_for_each_book():
        books = list_books(TEST_HOME)
        for book in books:
            assert "title" in book, f"Book missing title: {book}"
            assert "path" in book, f"Book missing path: {book}"
            assert "author" in book, f"Book missing author: {book}"
            assert "updated" in book, f"Book missing updated date: {book}"


def describe_find_book_by_title():
    def it_finds_book_by_exact_title():
        book = find_book_by_title(
            "Growing Object-Oriented Software, Guided by Tests", TEST_HOME
        )
        assert book is not None, "Test book not found"
        assert "401429854.epub" in book["path"], "Found incorrect book"

    def it_returns_none_when_book_not_found():
        book = find_book_by_title("Non-existent Book Title", TEST_HOME)
        assert book is None, "Expected None for non-existent book"


def describe_list_recent_books():
    def it_returns_books_with_reading_progress():
        books = list_recent_books(TEST_HOME)
        assert len(books) > 0, "Expected to find recent books"

        for book in books:
            assert "title" in book, f"Book missing title: {book}"
            assert "author" in book, f"Book missing author: {book}"
            assert (
                "reading_progress_percentage" in book
            ), f"Book missing reading_progress_percentage: {book}"
