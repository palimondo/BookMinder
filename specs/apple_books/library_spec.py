import os


def describe_book_library():
    def describe_when_listing_books():
        def it_finds_books_from_apple_books_directory():
            from bookminder.apple_books.library import list_books

            books = list_books()
            assert len(books) > 0, "Expected to find at least one book"

        def it_includes_basic_metadata_for_each_book():
            from bookminder.apple_books.library import list_books

            books = list_books()
            for book in books:
                assert "title" in book, f"Book missing title: {book}"
                assert "path" in book, f"Book missing path: {book}"
                assert os.path.exists(
                    book["path"]
                ), f"Book path does not exist: {book['path']}"

        def it_can_find_specific_book_by_title():
            from bookminder.apple_books.library import find_book_by_title

            book = find_book_by_title(
                "Growing Object-Oriented Software, Guided by Tests"
            )
            assert book is not None, "Test book not found"
            assert "401429854.epub" in book["path"], "Found incorrect book"

        def it_can_sort_books_by_last_update_date():
            from bookminder.apple_books.library import list_books

            books = list_books(sort_by="updated")
            if len(books) >= 2:
                assert (
                    books[0]["updated"] >= books[1]["updated"]
                ), "Books not sorted correctly"
