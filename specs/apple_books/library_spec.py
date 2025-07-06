from pathlib import Path

from bookminder.apple_books.library import (
    _row_to_book,
    find_book_by_title,
    list_all_books,
    list_books,
    list_recent_books,
)

TEST_HOME = Path(__file__).parent / "fixtures/users/test_reader"


def row_stub(**overrides):
    """Create a dict stub for sqlite3.Row with minimal defaults."""
    defaults = {
        "ZTITLE": "Title",
        "ZAUTHOR": "Author",
        "ZLASTOPENDATE": 0.0,
        "ZREADINGPROGRESS": 0.0,
        "ZSTATE": 1,
        "ZISSAMPLE": 0,
    }
    return {**defaults, **overrides}  # type: ignore[return-value]


def describe_row_to_book():
    def it_correctly_identifies_cloud_and_sample_states():
        book = _row_to_book(row_stub(ZSTATE=1, ZISSAMPLE=0))
        assert book.get("is_cloud") is False
        assert book.get("is_sample") is False

        book = _row_to_book(row_stub(ZSTATE=1, ZISSAMPLE=1))
        assert book.get("is_cloud") is False
        assert book.get("is_sample") is True

        book = _row_to_book(row_stub(ZSTATE=3, ZISSAMPLE=0))
        assert book.get("is_cloud") is True
        assert book.get("is_sample") is False

        book = _row_to_book(row_stub(ZSTATE=6, ZISSAMPLE=0))
        assert book.get("is_cloud") is True
        assert book.get("is_sample") is True


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
            assert "reading_progress_percentage" in book, (
                f"Book missing reading_progress_percentage: {book}"
            )


def describe_list_all_books():
    def it_returns_all_books_in_library():
        books = list_all_books(TEST_HOME)

        assert len(books) > 3, "Expected more than 3 books in test fixture"

        # Check we have books with different states
        titles = [book["title"] for book in books]
        assert "Extreme Programming Explained" in titles  # Local book with progress
        assert "Lao Tzu: Tao Te Ching" in titles  # Cloud book with progress
        assert "Snow Crash" in titles  # Cloud sample
        assert "Tiny Experiments" in titles  # Local sample
        # TODO: finished book

    def it_includes_sample_status_in_book_data():
        books = list_all_books(TEST_HOME)

        sample_books = [
            b for b in books if b["title"] in ["Snow Crash", "Tiny Experiments"]
        ]
        assert len(sample_books) == 2, "Expected to find both sample books"

        for book in sample_books:
            assert "is_sample" in book, f"Expected is_sample field in {book['title']}"
            assert book["is_sample"] is True, (
                f"Expected {book['title']} to be marked as sample"
            )
