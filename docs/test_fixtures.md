# Test Fixtures Documentation

## Overview

This document describes the test fixtures used in BookMinder and how they were prepared.

## Apple Books Test Data

Location: `specs/apple_books/fixtures/`

### Purpose
To enable unit tests to run in CI environments without requiring Apple Books to be installed, we created minimal test fixtures that simulate the Apple Books library structure.

### Files

#### Books.plist
- **Source**: Extracted from real Apple Books library (`~/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books/Books.plist`)
- **Content**: Contains metadata for one book: "Growing Object-Oriented Software, Guided by Tests" 
- **Preparation**:
  1. Exported full Books.plist to XML format using `plutil`
  2. Extracted just the GOOS book entry using Python's plistlib
  3. Modified the `path` field to point to the fixture directory instead of the original Apple Books location
  4. Saved as minimal plist with single book entry

#### 401429854.epub
- **Purpose**: Empty placeholder file to satisfy path existence checks in `library.py`
- **Content**: Empty file (0 bytes)
- **Future**: Will be replaced with minimal valid EPUB containing basic structure and TOC when needed for testing EPUB parsing features

### Test Strategy

The test fixture is automatically used via pytest monkeypatch in `specs/apple_books/library_spec.py`:
- `BOOKS_PATH` is patched to point to the fixtures directory
- `BOOKS_PLIST` is patched to point to our test plist file
- This allows the same tests to run against predictable test data in all environments

### Maintenance Notes

When adding new test books:
1. Extract the book entry from a real Books.plist
2. Update the path to point to the fixtures directory
3. Create a placeholder EPUB file with matching filename
4. Document any special properties of the test book here

When implementing EPUB parsing features:
1. Replace empty placeholder with minimal valid EPUB
2. Include only necessary structure (mimetype, META-INF/container.xml, content.opf, toc.ncx)
3. Keep file size minimal while maintaining validity

## SQLite Database Fixture Management

To ensure test fixtures accurately reflect real-world Apple Books data, there are shell scripts to copy complete book entries from your main Apple Books database to test fixture databases. This method is robust as it directly transfers data between two SQLite databases with identical schemas.

The fixture management scripts located in `specs/apple_books/fixtures/` specifically handle the BKLibrary SQLite database fixtures:

### create_fixture.sh
This script creates a fresh, empty BKLibrary test fixture database for a specified user. It extracts the schema from your real Apple Books database to ensure consistency.

```bash
./specs/apple_books/fixtures/create_fixture.sh <username>
```

Example:
```bash
./specs/apple_books/fixtures/create_fixture.sh test_reader
```

This will create a `BKLibrary-fixture.sqlite` file within the `test_reader` user's fixture directory.

### copy_book_to_fixture.sh
After creating a fixture database, this script allows you to copy specific book entries from your real Apple Books BKLibrary database into the newly created fixture database. It dynamically extracts all column names to ensure a complete and accurate copy.

```bash
./specs/apple_books/fixtures/copy_book_to_fixture.sh <username> "<book_title>"
```

Example:
```bash
./specs/apple_books/fixtures/copy_book_to_fixture.sh test_reader "The Left Hand of Darkness"
```

Both scripts utilize `_common.sh` for shared path definitions.

This process ensures that your SQLite database test fixtures are isolated, reproducible, and accurately reflect the structure and data of your live Apple Books BKLibrary database.