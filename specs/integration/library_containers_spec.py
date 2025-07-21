"""Integration tests for Apple Books SQLite library with test fixtures."""

from pathlib import Path

import pytest

from bookminder import BookminderError
from bookminder.apple_books.library import (
    find_book_by_title,
    list_all_books,
    list_books,
    list_recent_books,
)

# Path to test fixtures
FIXTURE_PATH = (
    Path(__file__).parent.parent / "apple_books" / "fixtures" / "users"
).absolute()


def describe_library_edge_cases():
    def it_handles_user_who_never_opened_apple_books():
        """User has iBooksX container but no BKAgentService container."""
        with pytest.raises(BookminderError) as e:
            list_recent_books(FIXTURE_PATH / "never_opened_user")
        error_msg = str(e.value)
        assert "Apple Books database not found" in error_msg
        assert "No BKLibrary database found in:" in error_msg
        assert "iBooksX/Data/Documents/BKLibrary" in error_msg

    def it_handles_fresh_apple_books_user_with_no_books():
        """User opened Apple Books but has no books in library."""
        books = list_recent_books(FIXTURE_PATH / "fresh_books_user")
        assert books == []

    def it_handles_user_with_legacy_apple_books_installation():
        """User has Books.plist but missing BKLibrary database."""
        with pytest.raises(BookminderError) as e:
            list_recent_books(FIXTURE_PATH / "legacy_books_user")
        error_msg = str(e.value)
        assert "Apple Books database not found" in error_msg
        assert "BKLibrary directory not found:" in error_msg
        assert "iBooksX/Data/Documents/BKLibrary" in error_msg

    def it_handles_user_with_corrupted_apple_books_database():
        """Database file exists but is corrupted."""
        with pytest.raises(BookminderError) as e:
            list_recent_books(FIXTURE_PATH / "corrupted_db_user")
        assert "Error reading Apple Books database:" in str(e.value)

    def it_shows_books_for_user_with_reading_progress():
        books = list_recent_books(FIXTURE_PATH / "test_reader")

        assert len(books) > 0
        assert len(books) <= 10  # recent books limited to 10

        # Verify books have expected fields
        for book in books:
            assert book["title"]
            assert book["author"]
            assert "reading_progress_percentage" in book
            assert book["reading_progress_percentage"] > 0

        # Verify ordering (most recent first)
        assert books[0]["title"] == "Extreme Programming Explained"
        assert books[1]["title"] == "The Left Hand of Darkness"


def describe_list_all_books():
    def it_handles_fresh_apple_books_user_with_no_books():
        """User opened Apple Books but has no books in library."""
        books = list_all_books(FIXTURE_PATH / "fresh_books_user")
        assert books == []

    def it_shows_all_books_for_user():
        books = list_all_books(FIXTURE_PATH / "test_reader")

        assert len(books) > 0

        # Should include books with and without progress
        titles = {book["title"] for book in books}
        assert "Extreme Programming Explained" in titles  # Has progress
        assert "Snow Crash" in titles  # No progress
        assert "Tiny Experiments" in titles  # Sample


def describe_list_books():
    def it_finds_books_from_apple_books_directory():
        books = list_books(FIXTURE_PATH / "test_reader")
        assert len(books) > 0, "Expected to find at least one book"

    def it_includes_basic_metadata_for_each_book():
        books = list_books(FIXTURE_PATH / "test_reader")
        for book in books:
            assert "title" in book, f"Book missing title: {book}"
            assert "path" in book, f"Book missing path: {book}"
            assert "author" in book, f"Book missing author: {book}"
            assert "updated" in book, f"Book missing updated date: {book}"


def describe_find_book_by_title():
    def it_finds_book_by_exact_title():
        book = find_book_by_title(
            "Growing Object-Oriented Software, Guided by Tests",
            FIXTURE_PATH / "test_reader",
        )
        assert book is not None, "Test book not found"
        assert "401429854.epub" in book["path"], "Found incorrect book"

    def it_returns_none_when_book_not_found():
        book = find_book_by_title(
            "Non-existent Book Title", FIXTURE_PATH / "test_reader"
        )
        assert book is None, "Expected None for non-existent book"


def describe_list_recent_books_integration():
    def it_returns_books_with_reading_progress():
        books = list_recent_books(FIXTURE_PATH / "test_reader")
        assert len(books) > 0, "Expected to find recent books"

        for book in books:
            assert "title" in book, f"Book missing title: {book}"
            assert "author" in book, f"Book missing author: {book}"
            assert "reading_progress_percentage" in book, (
                f"Book missing reading_progress_percentage: {book}"
            )

    def it_filters_by_cloud_status():
        cloud_books = list_recent_books(FIXTURE_PATH / "test_reader", filter="cloud")
        assert len(cloud_books) > 0, "Expected to find cloud books"

        for book in cloud_books:
            assert book.get("is_cloud") is True, f"Expected cloud book: {book['title']}"

    def it_excludes_cloud_books_with_not_cloud_filter():
        non_cloud_books = list_recent_books(
            FIXTURE_PATH / "test_reader", filter="!cloud"
        )
        assert len(non_cloud_books) > 0, "Expected to find non-cloud books"

        for book in non_cloud_books:
            assert book.get("is_cloud") is not True, (
                f"Expected non-cloud book: {book['title']}"
            )

    def it_filters_by_sample_status():
        sample_books = list_recent_books(FIXTURE_PATH / "test_reader", filter="sample")

        for book in sample_books:
            assert book.get("is_sample") is True, \
                f"Expected sample book: {book['title']}"

    def it_excludes_samples_with_not_sample_filter():
        non_sample_books = list_recent_books(
            FIXTURE_PATH / "test_reader", filter="!sample"
        )

        for book in non_sample_books:
            assert book.get("is_sample") is False, \
                f"Found sample book in !sample filter: {book['title']}"


def describe_list_all_books_integration():
    def it_returns_all_books_in_library():
        books = list_all_books(FIXTURE_PATH / "test_reader")

        assert len(books) > 3, "Expected more than 3 books in test fixture"

        # Check we have books with different states
        titles = [book["title"] for book in books]
        assert "Extreme Programming Explained" in titles  # Local book with progress
        assert "Lao Tzu: Tao Te Ching" in titles  # Cloud book with progress
        assert "Snow Crash" in titles  # Cloud sample
        assert "Tiny Experiments" in titles  # Local sample

    def it_includes_sample_status_in_book_data():
        books = list_all_books(FIXTURE_PATH / "test_reader")

        sample_books = [
            b for b in books if b["title"] in ["Snow Crash", "Tiny Experiments"]
        ]
        assert len(sample_books) == 2, "Expected to find both sample books"

        for book in sample_books:
            assert "is_sample" in book, f"Expected is_sample field in {book['title']}"
            assert book["is_sample"] is True, (
                f"Expected {book['title']} to be marked as sample"
            )

    def it_filters_books_by_sample_status():
        sample_books = list_all_books(FIXTURE_PATH / "test_reader", filter="sample")

        sample_titles = {book["title"] for book in sample_books}
        expected_samples = {"Snow Crash", "Tiny Experiments", "What's Our Problem?"}

        assert sample_titles == expected_samples, \
            f"Expected {expected_samples}, got {sample_titles}"

    def it_excludes_samples_with_not_sample_filter():
        books = list_all_books(FIXTURE_PATH / "test_reader", filter="!sample")

        for book in books:
            assert book["is_sample"] is False, \
                f"Found sample book in !sample filter: {book['title']}"

        assert len(books) > 0, "Expected non-sample books to exist"
