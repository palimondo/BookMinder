# Apple Books Data Sources

This document describes the data sources used by Apple Books on macOS and how BookMinder accesses them.

## Overview

Apple Books stores data across multiple files and databases in different container directories. Understanding these data sources is crucial for extracting book metadata, reading progress, and activity information.

## Container Directories

Apple Books uses sandboxed containers to store its data:

- **com.apple.BKAgentService**: Contains the book files and basic catalog
- **com.apple.iBooksX**: Contains databases for reading progress, activity, and UI state

## Data Sources

### 1. Books.plist

**Location**: `/Users/{user}/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books/Books.plist`

**Purpose**: Primary book catalog with metadata

**Key Fields**:
- `itemName`: Book title
- `artistName`: Author name
- `path`: Relative path to EPUB file
- `updateDate`: Last modification date
- `BKPercentComplete`: Only present for **finished books** (always 1.0 = 100%)

**Important Discovery**:
- Contains all books in library (179 total in test case)
- Only 22 books have `BKPercentComplete` field (12% of library)
- All books with `BKPercentComplete` show 1.0 (100% complete)
- Books without this field are either unread or partially read
- **Does NOT contain actual reading progress for books in progress**

### 2. BKLibrary SQLite Database

**Location Pattern**: `/Users/{user}/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/BKLibrary-*.sqlite`

**Note**: The filename contains variable numbers (e.g., `BKLibrary-1-091020131601.sqlite`) that change between installations. Use glob pattern matching to locate.

**Purpose**: Complete library database with reading progress and activity

**Key Table**: `ZBKLIBRARYASSET`

**Critical Fields for Reading Progress**:
- `ZTITLE`: Book title
- `ZAUTHOR`: Author name  
- `ZASSETID`: Asset identifier (matches Books.plist keys)
- `ZREADINGPROGRESS`: Float value (0.0 to 1.0) representing actual reading progress
- `ZLASTOPENDATE`: Timestamp when book was last opened (Apple reference date)
- `ZISFINISHED`: Integer indicating if book is finished (1 = finished, 0 = not finished)
- `ZDATEFINISHED`: Timestamp when book was finished
- `ZCREATIONDATE`: When book was added to library

**Additional Important Fields**:
- `ZISSAMPLE`: Integer indicating if book is a sample (1 = sample, 0 = full book)
- `ZCONTENTTYPE`: Integer indicating content type (likely: 1 = Book, 3 = PDF)
- `ZPATH`: Path to the book file (relative to Books directory)
- `ZFILESIZE`: Size of the book file in bytes
- `ZSTATE`: Integer indicating download/availability state
- `ZGENRE`: Book genre/category
- `ZKIND`: Content kind (e.g., "ebook", "pdf")
- `ZPAGECOUNT`: Number of pages in the book
- `ZISEPHEMERAL`: Integer indicating temporary status

**Example Query for Recent Books**:
```sql
SELECT ZTITLE, ZAUTHOR, ZREADINGPROGRESS, ZLASTOPENDATE, ZISFINISHED 
FROM ZBKLIBRARYASSET 
WHERE ZREADINGPROGRESS > 0 
ORDER BY ZLASTOPENDATE DESC 
LIMIT 10;
```

**Sample Results**:
- "The Left Hand of Darkness" - Ursula K. Le Guin - 32% progress
- "Lao Tzu: Tao Te Ching" - Ursula K. Le Guin - 8% progress  
- "The Beginning of Infinity" - David Deutsch - 59% progress

### 3. Recently Opened Books Database

**Location**: `/Users/{user}/Library/Containers/com.apple.iBooksX/Data/Documents/BCRecentlyOpenedBooksDB/BCRecentlyOpenedBooksDB.sqlite`

**Note**: This filename appears to be fixed (no variable numbers).

**Purpose**: Tracks reading sessions and activity

**Key Table**: `ZBCASSETREADINGSESSION`

**Fields**:
- `ZASSETID`: Asset identifier
- `ZTIMEOPENED`: When reading session started (Apple reference date)
- `ZTIMECLOSED`: When reading session ended
- `ZTIMEUPDATED`: Last update timestamp

## Data Relationships

### Asset ID Mapping
- Books.plist uses keys like "401429854" (numeric strings)
- BKLibrary database uses same IDs in `ZASSETID` field
- Reading sessions reference same IDs in `ZASSETID`

### Progress Data Sources Hierarchy
1. **BKLibrary.sqlite** - Authoritative source for reading progress (ZREADINGPROGRESS 0.0-1.0)
2. **Books.plist** - Only shows finished books (BKPercentComplete = 1.0)
3. **Reading sessions** - Activity timestamps but no progress percentages

### Content Type Identification

**In BKLibrary Database**:
- `ZCONTENTTYPE = 1`: Regular books (EPUB)
- `ZCONTENTTYPE = 3`: PDF documents  
- `ZISSAMPLE = 1`: Sample/preview books
- `ZKIND = "ebook"`: Standard ebook format
- `ZKIND = "pdf"`: PDF document

**In Books.plist**:
- `kind = "ebook"`: EPUB books
- `fileExtension = "epub"`: EPUB format
- `BKBookType = "epub"`: Book type identifier

### Asset ID Correlation System

Asset IDs provide the link between different data sources:

**Format**: Numeric strings (e.g., "401429854", "1296850431")

**Cross-Reference Pattern**:
```
Books.plist key: "401429854"
    ↓
BKLibrary.ZASSETID: "401429854"  
    ↓
Reading Session.ZASSETID: "401429854"
    ↓
File path: "401429854.epub"
```

**Asset ID Sources**:
- iTunes Store ID for purchased books
- Generated ID for sideloaded content  
- Hexadecimal IDs for some system content (e.g., "1F150082C5E6CD9413FAA197989BC910")

### Apple Timestamp Format Details

Apple uses Core Data timestamp format with reference date January 1, 2001, 00:00:00 UTC.

**Conversion Examples**:
```python
# Raw timestamp: 772198715.562895
# Converts to: 2025-06-22 20:11:55 UTC

def apple_to_unix_timestamp(apple_timestamp):
    # Apple epoch: January 1, 2001 UTC
    # Unix epoch: January 1, 1970 UTC  
    # Difference: 978307200 seconds (31 years)
    return apple_timestamp + 978307200

def apple_timestamp_to_datetime(apple_timestamp):
    apple_epoch = datetime.datetime(2001, 1, 1, tzinfo=datetime.timezone.utc)
    return apple_epoch + datetime.timedelta(seconds=apple_timestamp)
```

**Common Timestamp Fields**:
- `ZLASTOPENDATE`: When book was last opened
- `ZDATEFINISHED`: When book was completed
- `ZCREATIONDATE`: When book was added to library
- `updateDate` (Books.plist): Last modification (ISO format)

### Database Performance and Access

**File Structure**:
- Main database: `BKLibrary-*.sqlite`
- Write-Ahead Log: `BKLibrary-*.sqlite-wal` 
- Shared Memory: `BKLibrary-*.sqlite-shm`

**Access Pattern**:
- Query the main `.sqlite` file
- SQLite automatically handles WAL/SHM files
- Database may be locked during active Apple Books usage

**Recommended Query Approach**:
```python
import sqlite3
import glob

# Locate database
pattern = f"{home}/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/BKLibrary-*.sqlite"
db_files = glob.glob(pattern)
if not db_files:
    raise FileNotFoundError("BKLibrary database not found")

db_path = db_files[0]  # Use first match

# Query with error handling
try:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()
        # Execute queries...
except sqlite3.OperationalError as e:
    if "database is locked" in str(e):
        # Apple Books is running, retry or prompt user
        pass
```

## Apple Books UI Analysis

### UI Structure Overview

Apple Books organizes content in the Home screen with distinct sections that correlate directly to database states:

1. **Continue Section**: Currently reading books (progress 1-99%)
2. **Previous Section**: All previously accessed books (mixed states)
3. **Books Read This Year**: Achievement view (finished books only)

### Content Types and Indicators

**Content Types**:
- **Book**: Regular ebooks (EPUB format)
- **PDF**: Technical documents, manuals, papers
- **Sample**: Free previews from the bookstore

**Status Indicators**:
- **Percentage (1%-99%)**: Active reading progress
- **"Finished" + blue checkmark**: Completed books (100%)
- **"Sample"**: Preview/trial versions
- **Cloud icon**: Books stored in iCloud but not downloaded locally

### Detailed Section Analysis

#### Continue Section (10 books visible)
Books currently being read, sorted by recent activity. All show percentage progress:

| Title | Author | Progress | Type | Cloud |
|-------|--------|----------|------|-------|
| The Left Hand of Darkness | Ursula K. Le Guin & Charlie Jane Anders | 32% | Book | No |
| Lao Tzu: Tao Te Ching | Ursula K. Le Guin | 8% | Book | Yes |
| Tao Te Ching | Laozi | 3% | Book | Yes |
| Quicksilver | Neal Stephenson | 4% | Book | Yes |
| The Beginning of Infinity | David Deutsch | 59% | Book | No |
| User Story Mapping | Jeff Patton | 21% | Book | No |
| Growing Object-Oriented Software, Guided by Tests | Steve Freeman | 8% | Book | No |
| A Clockwork Orange | Anthony Burgess | 1% | Book | No |
| The Canon of Reason and Virtue | Paul Carus Daisetsu... | 14% | Book | Yes |
| record-layer-paper | Christos Chrysa... | 1% | PDF | Yes |

#### Previous Section
Mixed collection of all previously accessed books with various states.

![Previous Section - List View](Previous%20list.jpg)
![Previous Section - List View Page 2](Previous%20list%20p2.jpg)
![Previous Section - Tile View](Previous%20tiles.jpg)

**Partial Progress Books**:
- Tiny Experiments - Anne-Laure Le Cunff (1%) Book • Sample
- Manual_Melitta_Purista_CZ_SK - ZINDEL AG (83%) PDF
- Mechanický pomaranč - Anthony Burgess (4%) Book
- A Clockwork Orange - Anthony Burgess & Andrew Biswell (96%) Book
- Quicksilver - Neal Stephenson (4%) Book • Cloud
- Twelve Tomorrows - Neil Stephenson, David Brin, etc. (4%) Book • Cloud
- The Scaling Era - Dwarkesh Patel (1%) Book
- Automobil v podnikaní režimy a tipy Ľudskou Rečou sk v2023 - Unknown Author (4%) PDF • Cloud
- Working Effectively with Legacy Code - Michael C. Feathers (2%) Book
- Refactoring - Martin Fowler (2%) Book
- Extreme Programming Explained - Kent Beck & Cynthia Andres (69%) Book
- REST in Practice - Jim Webber, Savas Parastatidis, and Ian Robinson (5%) Book
- Stubborn Attachments - Tyler Cowen (4%) Book

**Finished Books**:
- MELITTA CAFFEO SOLO - Unknown Author PDF • Finished
- Artificial Intelligence - Tim Rocktäschel Book • Finished
- The Coming Wave - Mustafa Suleyman & Michael Bhaskar Book • Finished
- Attack Surface - Cory Doctorow Book • Finished
- Red Team Blues - Cory Doctorow Book • Finished

**Sample Books**:
- Snow Crash - Neal Stephenson Book • Sample
- What's Our Problem? - Tim Urban Book • Sample • Cloud

**No Progress Shown**:
- Postman - Technopoly - Neil Postman PDF
- For The Win - Cory Doctorow Book

#### Books Read This Year Section (4 books)
Achievement-focused view showing only completed books:
- Attack Surface - Cory Doctorow
- Red Team Blues - Cory Doctorow
- Chip War - Chris Miller  
- The Diamond Age - Neal Stephenson

**Status**: "Yearly Goal Achieved - 4 books finished. Keep reading!"

### Database to UI Mapping

#### Continue Section = Recent Reading Activity
**Database Query**:
```sql
SELECT * FROM ZBKLIBRARYASSET 
WHERE ZREADINGPROGRESS > 0 AND ZREADINGPROGRESS < 1.0
ORDER BY ZLASTOPENDATE DESC 
LIMIT 10;
```

#### Previous Section = All Library Content
**Database Query**:
```sql
SELECT * FROM ZBKLIBRARYASSET 
ORDER BY ZLASTOPENDATE DESC;
```

#### Books Read This Year = Finished Books
**Database Query**:
```sql
SELECT * FROM ZBKLIBRARYASSET 
WHERE ZISFINISHED = 1 
AND ZDATEFINISHED >= [start_of_year_timestamp]
ORDER BY ZDATEFINISHED DESC;
```

### Validation Test Cases

Use these specific books to validate database queries match UI display:

**Top 3 Continue Section Books**:
1. "The Left Hand of Darkness" → Should show ~32% progress
2. "Lao Tzu: Tao Te Ching" → Should show ~8% progress  
3. "Tao Te Ching" → Should show ~3% progress

**Sample Books** (should have special handling):
- "Tiny Experiments" → Sample with 1% progress
- "Snow Crash" → Sample with no progress shown
- "What's Our Problem?" → Sample with no progress shown

**Finished Books** (should appear in year view):
- "Attack Surface", "Red Team Blues", "Chip War", "The Diamond Age"

**PDF Content**:
- "Manual_Melitta_Purista_CZ_SK" → 83% progress
- "record-layer-paper" → 1% progress
- "MELITTA CAFFEO SOLO" → Finished
- "Postman - Technopoly" → No progress

**High Progress Books**:
- "A Clockwork Orange" (Anthony Burgess & Andrew Biswell) → 96%
- "Reentry" → 82%
- "Extreme Programming Explained" → 69%

### UI Behavior Insights

1. **Continue section prioritizes active reading** (1-99% progress, recent activity)
2. **Previous section shows reading history** (all states, sorted by last access)
3. **Cloud status affects availability** but not progress tracking
4. **Sample books can show progress** but are marked distinctly
5. **PDF documents integrate seamlessly** with book progress tracking
6. **Finished books appear in multiple sections** (Previous + Year view)
7. **Zero progress books still appear in Previous** if accessed before

## Implementation Strategy for "Recent Books"

To implement `bookminder list recent` with accurate progress percentages:

### Step 1: Locate Database
```python
import glob
db_pattern = f"{home}/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/BKLibrary-*.sqlite"
db_path = glob.glob(db_pattern)[0]  # Get first match
```

### Step 2: Query Reading Progress
```sql
SELECT 
    ZTITLE,
    ZAUTHOR, 
    ZREADINGPROGRESS * 100 as PROGRESS_PERCENT,
    ZLASTOPENDATE
FROM ZBKLIBRARYASSET 
WHERE ZREADINGPROGRESS > 0 
ORDER BY ZLASTOPENDATE DESC 
LIMIT 10;
```

### Step 3: Convert Apple Timestamps
Apple uses reference date of January 1, 2001 (Core Data timestamp format).

```python
import datetime
def apple_timestamp_to_datetime(timestamp):
    apple_epoch = datetime.datetime(2001, 1, 1)
    return apple_epoch + datetime.timedelta(seconds=timestamp)
```

### Step 4: Format Output
```
The Left Hand of Darkness - Ursula K. Le Guin (32%)
Lao Tzu: Tao Te Ching - Ursula K. Le Guin (8%)
The Beginning of Infinity - David Deutsch (59%)
```

## User State Scenarios

Through real-world testing on macOS, we discovered distinct Apple Books states for different users:

### 1. Never Opened Apple Books
**Containers Present**: 
- `com.apple.iBooksX` (created automatically by macOS)
- No `com.apple.BKAgentService` container

**Files Present**: None

**Key Insight**: The iBooksX container is created during user account setup, not when Apple Books is first opened.

### 2. Fresh Apple Books (Just Opened, No Books)
**Containers Present**: Both containers exist
- `com.apple.BKAgentService` (created when Apple Books first launches)
- `com.apple.iBooksX`

**Files Present**:
- `Books.plist` with empty books array
- `BKLibrary-*.sqlite` database with 0 rows in ZBKLIBRARYASSET table

**Key Insight**: Apple Books creates all infrastructure immediately upon first launch, including the SQLite database.

### 3. Legacy/Edge Case Installation
**Example**: User "katka" from testing
- Containers from 2020-2021
- Has `Books.plist` (empty)
- Missing `BKLibrary` directory entirely

**Possible Causes**:
- Older Apple Books version
- Migration issues
- Manual cleanup

### 4. Active Reader
**All infrastructure present** with actual book data and reading progress.

## Database Discovery Timeline

This information was discovered through systematic investigation:

1. **Initial Books.plist analysis**: Found only completed books (BKPercentComplete)
2. **Apple Books UI screenshots**: Revealed granular progress tracking (1-99%)
3. **File system exploration**: Located SQLite databases in iBooksX container
4. **Database schema analysis**: Found ZREADINGPROGRESS field with float values
5. **Data correlation**: Confirmed BKLibrary.sqlite as authoritative progress source
6. **Filename pattern discovery**: Identified variable numbers in database names
7. **User state validation**: Tested multiple user accounts to understand container creation

## Edge Cases and Special Considerations

### Progress Edge Cases
- **Zero progress books**: May exist in library but never opened (ZREADINGPROGRESS = 0.0)
- **Null progress**: Some books may have NULL progress values
- **Finished books**: Always show ZREADINGPROGRESS = 1.0 AND ZISFINISHED = 1
- **Sample books**: Can have partial progress but remain samples (ZISSAMPLE = 1)

### Content Type Edge Cases  
- **Mixed format books**: Some books may have mismatched file extensions
- **System content**: Hexadecimal asset IDs for system/default content
- **Corrupted entries**: Books with missing file paths or invalid metadata
- **iCloud books**: Books in cloud but not downloaded locally (check ZSTATE)

### Timestamp Edge Cases
- **Null timestamps**: Books may have NULL values for ZLASTOPENDATE
- **Future timestamps**: Possible due to timezone issues or system clock problems
- **Zero timestamps**: Apple epoch (2001-01-01) indicates unset values

### Database Access Issues
- **Missing databases**: User hasn't used Apple Books, fresh installation
- **Permission errors**: Sandboxing restrictions, SIP protections
- **Database locks**: Apple Books actively using database
- **Schema changes**: Apple Books updates may modify database structure
- **Multiple versions**: User might have multiple BKLibrary databases

### Sample Book Handling
```sql
-- Get samples separately as they behave differently
SELECT * FROM ZBKLIBRARYASSET 
WHERE ZISSAMPLE = 1 
AND ZREADINGPROGRESS > 0
ORDER BY ZLASTOPENDATE DESC;
```

### Content Filtering Strategies
```sql
-- Active reading (excluding samples and finished)
SELECT * FROM ZBKLIBRARYASSET 
WHERE ZREADINGPROGRESS > 0 
AND ZREADINGPROGRESS < 1.0 
AND (ZISSAMPLE IS NULL OR ZISSAMPLE = 0)
ORDER BY ZLASTOPENDATE DESC;

-- Include samples in recent reading  
SELECT * FROM ZBKLIBRARYASSET 
WHERE ZREADINGPROGRESS > 0
ORDER BY ZLASTOPENDATE DESC;

-- Only finished books this year
SELECT * FROM ZBKLIBRARYASSET 
WHERE ZISFINISHED = 1 
AND ZDATEFINISHED > [year_start_timestamp]
ORDER BY ZDATEFINISHED DESC;
```

## Critical Implementation Notes

- **Use glob patterns** for database discovery (filenames contain variable numbers)
- **BKLibrary.sqlite is authoritative** for reading progress, not Books.plist
- **Reading progress stored as float** (0.0 to 1.0), multiply by 100 for percentages
- **Use ZLASTOPENDATE for recency**, not updateDate from Books.plist
- **Apple timestamps** use 2001-01-01 as epoch, not Unix epoch
- **Database files include WAL/SHM** files (Write-Ahead Logging) - query main .sqlite file
- **Handle NULL values** gracefully in all timestamp and progress fields
- **Check ZISSAMPLE flag** to identify preview/trial books
- **Use ZCONTENTTYPE** to distinguish between books and PDFs
- **Implement retry logic** for database lock errors
- **Validate asset ID format** before cross-referencing with Books.plist

## Future Considerations

- Monitor for database schema changes across Apple Books versions
- Consider reading session data for more detailed activity analysis
- Handle potential permission issues accessing sandboxed containers
- Test across different macOS versions and Apple Books versions

# BookMinder Domain Language and CLI Mapping

To ensure clarity and consistency in BookMinder's development and user interface, we define the following domain language, directly mapped to Apple Books' internal data structures.

## 1. Content Type (What is it?)

Describes the fundamental format or origin of the content.

-   **Book (EPUB):** A standard e-book, typically from the Apple Books store or sideloaded.
    -   *Mapping:* `BKLibrary.sqlite` where `ZCONTENTTYPE = 1` or `ZKIND = "ebook"`.
-   **PDF:** A Portable Document Format file.
    -   *Mapping:* `BKLibrary.sqlite` where `ZCONTENTTYPE = 3` or `ZKIND = "pdf"`.
-   **Audiobook:** (Future content type if data becomes available).

## 2. Reading Status (Where am I with it?)

Describes the user's progress through the content. This is a critical aspect for filtering and display.

-   **Finished:** The book is marked as complete by Apple Books.
    -   *Mapping:* `BKLibrary.sqlite` where `ZISFINISHED = 1`.
    -   *Note:* Empirical research shows that `ZREADINGPROGRESS` may or may not be `1.0` for finished books. However, if `ZREADINGPROGRESS` is `1.0`, then `ZISFINISHED` is also `1`.
-   **In Progress:** The book has some reading progress but is not marked as finished.
    -   *Mapping:* `BKLibrary.sqlite` where `ZREADINGPROGRESS > 0.0` AND `ZISFINISHED = 0`.
-   **Not Started:** The book has 0% reading progress and is not marked as finished.
    -   *Mapping:* `BKLibrary.sqlite` where `ZREADINGPROGRESS = 0.0` AND `ZISFINISHED = 0`.

## 3. Attributes/Flags (Other characteristics?)

Additional properties that can apply to any content type or reading status.

-   **Sample:** A preview version of a book.
    -   *Mapping:* `BKLibrary.sqlite` where `ZISSAMPLE = 1`.
-   **Cloud:** The book is stored in iCloud and may or may not be downloaded locally.
    -   *Mapping:* `BKLibrary.sqlite` where `ZSTATE` indicates cloud status.
    -   *Observed `ZSTATE` values:* `None`, `1`, `3`, `5`, `6`. Further empirical observation of Apple Books UI behavior and file system presence is needed to definitively map these values to "Cloud" status.
        *   **Update (2025-06-27):** `ZSTATE = 5` has been observed in conjunction with "Series" in the Apple Books UI (e.g., "Hainish", "The Baroque Cycle"). This suggests `ZSTATE = 5` might indicate a series or collection, rather than a cloud-only status. Further research is needed to confirm the definitive mapping for cloud status.

## CLI Mapping (Proposed Commands)

This section outlines how the domain language translates into user-facing CLI commands.

-   **`bookminder list` (Default: `recent`):** Shows "In Progress" books, ordered by `ZLASTOPENDATE`, limited to 10.
-   **`bookminder list all`:** Shows all books in the library, regardless of reading status, ordered by `ZLASTOPENDATE`. (Maps to Apple Books "Previous Section").
-   **Filtering by Reading Status (`--status` option):**
    -   `bookminder list --status finished`
    -   `bookminder list --status not-started`
    -   `bookminder list --status in-progress`
-   **Filtering by Content Type (`--type` option):**
    -   `bookminder list --type book`
    -   `bookminder list --type pdf`
-   **Filtering by Attributes (`--flag` option):**
    -   `bookminder list --flag sample`
    -   `bookminder list --flag cloud`
-   **Filtering by Time (`--year` option):**
    -   `bookminder list --year <YYYY>` (e.g., `2024`, `current`)
-   **Pagination (`--limit`, `--offset`):**
    -   `bookminder list all --limit 20`
    -   `bookminder list all --offset 20 --limit 20`
