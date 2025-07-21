from pathlib import Path

from bookminder.apple_books.library import (
    _build_books_query,
    _get_user_path,
    _row_to_book,
)

TEST_HOME = Path(__file__).parent / "fixtures/users/test_reader"


def describe_supported_filters():
    def it_exports_supported_filter_values():
        from bookminder.apple_books.library import SUPPORTED_FILTERS

        assert isinstance(SUPPORTED_FILTERS, set)
        assert SUPPORTED_FILTERS == {"cloud", "!cloud", "sample", "!sample"}


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


def describe_get_user_path():
    def it_returns_home_path_when_user_is_none():
        result = _get_user_path(None)
        assert result == Path.home()

    def it_converts_simple_username_to_users_path():
        result = _get_user_path("bob")
        assert result == Path("/Users/bob")

    def it_preserves_absolute_paths_for_fixtures():
        fixture_path = str(TEST_HOME)
        result = _get_user_path(fixture_path)
        assert result == Path(fixture_path)


def describe_build_books_query():
    def it_includes_required_columns_for_book_attributes():
        query = _build_books_query()

        # Verify all required columns are present
        assert "ZTITLE" in query, "Query must include ZTITLE for book title"
        assert "ZAUTHOR" in query, "Query must include ZAUTHOR for book author"
        assert "ZREADINGPROGRESS" in query, \
            "Query must include ZREADINGPROGRESS for reading percentage"
        assert "ZLASTOPENDATE" in query, \
            "Query must include ZLASTOPENDATE for updated timestamp"
        assert "ZSTATE" in query, "Query must include ZSTATE for cloud/sample status"
        assert "ZISSAMPLE" in query, \
            "Query must include ZISSAMPLE for sample identification"

    def it_applies_where_clause_and_limit():
        query = _build_books_query("WHERE ZREADINGPROGRESS > 0", limit=5)

        assert "WHERE ZREADINGPROGRESS > 0" in query
        assert "LIMIT 5" in query
        assert query.index("WHERE") < query.index("ORDER BY")
        assert query.index("ORDER BY") < query.index("LIMIT")


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
