#!/bin/zsh

# Creates a fresh, empty test fixture database with a consistent name and correct schema.
# Usage: ./create_fixture.sh <username>

set -e

FIXTURE_USER=$1
if [[ -z "$FIXTURE_USER" ]]; then
  echo "Usage: $0 <username>"
  exit 1
fi

source "$(dirname "$0")/_common.sh"

# --- Define Paths ---
echo "DEBUG: Searching for real DB in: [$HOME/$BKLIBRARY_USER_SUBPATH]"
REAL_DB_PATH=$(find "$HOME/$BKLIBRARY_USER_SUBPATH" -name "BKLibrary-*.sqlite" | head -n 1)
echo "DEBUG: REAL_DB_PATH resolved to: [$REAL_DB_PATH]"
if [[ ! -f "$REAL_DB_PATH" ]]; then
    echo "Error: Real Apple Books database not found. Find command returned empty."
    exit 1
fi

FIXTURE_DIR="$PROJECT_ROOT/$BKLIBRARY_FIXTURE_SUBPATH/$FIXTURE_USER/$BKLIBRARY_USER_SUBPATH"
# Use a consistent, predictable name for the fixture database.
FIXTURE_DB_PATH="$FIXTURE_DIR/BKLibrary-fixture.sqlite"

# --- Main Logic ---
echo "Creating new fixture for user: $FIXTURE_USER"

mkdir -p "$FIXTURE_DIR"

SCHEMA=$(sqlite3 "$REAL_DB_PATH" ".schema ZBKLIBRARYASSET")
if [[ -z "$SCHEMA" ]]; then
    echo "Error: Could not extract schema from real database."
    exit 1
fi

echo "Applying schema from real database..."
sqlite3 "$FIXTURE_DB_PATH" "$SCHEMA"

echo "✔ Fixture database created successfully at $FIXTURE_DB_PATH"