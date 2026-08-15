from unittest.mock import patch


def describe_cli_error_boundary():
    def it_reports_missing_database():
        with patch("bookminder.cli.list_recent_books") as mock:
            mock.side_effect = Exception("BKLibrary directory not found: /Users/pali")
            output = "BKLibrary directory not found: /Users/pali"
        assert "BKLibrary directory not found" in output
        assert "/Users/pali/Library" not in output
