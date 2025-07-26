import subprocess
import sys
from pathlib import Path


def _run_cli_with_user(user_name, use_fixture=True, subcommand="recent", filter=None):
    if use_fixture:
        integration_dir = Path(__file__).parent.parent / "integration"
        fixture_path = integration_dir / "apple_books/fixtures/users"
        user_arg = str(fixture_path / user_name)
    else:
        user_arg = user_name

    command = [
        sys.executable,
        "-m",
        "bookminder",
        "list",
        subcommand,
        "--user",
        user_arg,
    ]

    if filter:
        command.extend(["--filter", filter])

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent.parent,
    )
    assert result.returncode == 0, \
        f"Expected exit code 0, got {result.returncode}: {result.stderr}"
    return result


def describe_bookminder_integration():
    def it_shows_books_for_user_with_reading_progress():
        """Integration test: verify full stack works with real fixture."""
        result = _run_cli_with_user("test_reader")

        output_lines = result.stdout.strip().split("\n")
        assert len(output_lines) > 0, "Expected books in output"

        for line in output_lines:
            if line.strip():
                assert " - " in line, f"Expected 'Title - Author' format in: {line}"
                # Books can show either progress percentage or (Finished) status
                assert ("%" in line or "(Finished)" in line), (
                    f"Expected progress or finished status in: {line}"
                )
