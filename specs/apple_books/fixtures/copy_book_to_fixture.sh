#!/bin/zsh

# Copies a complete book entry from the real Apple Books database to a test fixture.
# Usage: ./copy_book_to_fixture.sh <username> "<book_title>"

set -e

FIXTURE_USER=$1
BOOK_TITLE=$2

if [[ -z "$FIXTURE_USER" || -z "$BOOK_TITLE" ]]; then
  echo "Usage: $0 <username> \"<book_title>\""
  exit 1
fi

source "$(dirname "$0")/_common.sh"

# --- Define Paths ---
REAL_DB_PATH=$(find "$HOME/$BKLIBRARY_USER_SUBPATH" -name "BKLibrary-*.sqlite" | head -n 1)
if [[ ! -f "$REAL_DB_PATH" ]]; then
    echo "Error: Real Apple Books database not found."
    exit 1
fi

FIXTURE_DIR="$PROJECT_ROOT/$BKLIBRARY_FIXTURE_SUBPATH/$FIXTURE_USER/$BKLIBRARY_USER_SUBPATH"
# Dynamically find the fixture DB, just like the python code does.
FIXTURE_DB_PATH=$(find "$FIXTURE_DIR" -name "BKLibrary-*.sqlite" | head -n 1)
if [[ ! -f "$FIXTURE_DB_PATH" ]]; then
    echo "Error: Fixture database for user '$FIXTURE_USER' not found. Please create it first with create_fixture.sh"
    exit 1
fi

# --- Dynamic Column Extraction ---
# Get all column names from ZBKLIBRARYASSET table, excluding Z_PK
COLUMNS_EXCL_PK=$(sqlite3 "$REAL_DB_PATH" "PRAGMA table_info(ZBKLIBRARYASSET);" | awk -F'|' '{print $2}' | grep -v '^Z_PK$' | tr '\n' ',' | sed 's/,$//')
if [[ -z "$COLUMNS_EXCL_PK" ]]; then
  echo "Error: Could not extract column names from real database."
  exit 1
fi

# --- Core Copy Logic ---
echo "Copying \"$BOOK_TITLE\" to fixture for user \"$FIXTURE_USER\"..."

# Escape single quotes in book title for SQL (double them for SQL)
ESCAPED_BOOK_TITLE="${BOOK_TITLE//\'/''}"

# Use ATTACH DATABASE for a robust, cross-database copy.
sqlite3 "$FIXTURE_DB_PATH" \
  "ATTACH DATABASE '$REAL_DB_PATH' AS real_db; \
   INSERT INTO ZBKLIBRARYASSET ($COLUMNS_EXCL_PK) \
   SELECT $COLUMNS_EXCL_PK FROM real_db.ZBKLIBRARYASSET WHERE ZTITLE = '$ESCAPED_BOOK_TITLE'; \
   DETACH DATABASE real_db;"

echo "✔ Successfully copied \"$BOOK_TITLE\" to fixture."