"""Synthetic violating fixture: library layer for boundary-text and dup-constant checks."""

SUPPORTED_FILTERS = {"cloud", "!cloud", "sample", "!sample"}


class BookminderError(Exception):
    pass


def list_recent_books(user_home):
    raise BookminderError(f"BKLibrary directory not found: {user_home}")
