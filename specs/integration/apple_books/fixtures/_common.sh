#!/bin/zsh

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" &>/dev/null && pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/../../.." && pwd)

BKLIBRARY_FIXTURE_SUBPATH="specs/apple_books/fixtures/users"
BKLIBRARY_USER_SUBPATH="Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary"
