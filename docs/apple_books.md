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
- `updateDate`: Timestamp of unestablished meaning - probably the publisher's revision date for the book, not reading activity
- `BKPercentComplete`: Only present for **finished books** (always 1.0 = 100%)

**Important Discovery**:
- **Not a complete catalog of the library**: titles the BKLibrary database knew about were missing from this file even in a freshly converted snapshot (e.g. "Lao Tzu: Tao Te Ching"), and the reason was never established - absence from Books.plist proves nothing about library membership or cloud status
- 179 entries in the test case, of which only 22 have the `BKPercentComplete` field (12%)
- All books with `BKPercentComplete` show 1.0 (100% complete)
- Books without this field are either unread or partially read
- **Does NOT contain actual reading progress for books in progress**

### 2. BKLibrary SQLite Database

**Location Pattern**: `/Users/{user}/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/BKLibrary-*.sqlite`

**Note**: The filename contains variable numbers (e.g., `BKLibrary-1-091020131601.sqlite`) that change between installations. Use glob pattern matching to locate.

**Purpose**: Complete library database with reading progress and activity

**Key Table**: `ZBKLIBRARYASSET`

**Critical Fields for Reading Progress**:
- `ZTITLE`: Book title - not a unique key: one title can occupy several rows, observed at different `ZSTATE` values and in one case under two different author strings. That case is two genuinely distinct editions of the same title in one library - separate covers, separate reading progress - as the UI itself shows (iPhone):

  ![In Your Library - two editions of A Clockwork Orange](ui/apple/In%20Your%20Library%20duplicate%20editions%20iPhone.png)
- `ZAUTHOR`: Author name
- `ZASSETID`: Asset identifier (matches Books.plist keys)
- `ZREADINGPROGRESS`: Float value (0.0 to 1.0) representing actual reading progress
- `ZLASTOPENDATE`: Timestamp when book was last opened (Apple reference date)
- `ZISFINISHED`: Integer indicating if book is finished (1 = finished, 0 = not finished)
- `ZDATEFINISHED`: Timestamp when book was finished
- `ZCREATIONDATE`: When book was added to library

**Additional Important Fields**:
- `ZISSAMPLE`: Integer flag carried by downloaded samples (1 = sample); 0 does not mean the book is not a sample - see [Sample Book Handling](#sample-book-handling)
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
- `ZCONTENTTYPE = 1`: Likely regular books (EPUB) - unverified against a live database
- `ZCONTENTTYPE = 3`: Likely PDF documents - unverified against a live database
- `ZISSAMPLE = 1`: Downloaded samples - samples are not identified by this flag alone, see [Sample Book Handling](#sample-book-handling)
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
- `updateDate` (Books.plist): ISO-format timestamp, probably a publisher revision date rather than reading activity

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

### Test Fixtures

For information on creating and managing test fixtures (including Books.plist, EPUB files, and SQLite databases), see [test_fixtures.md](test_fixtures.md).


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

#### Continue Section
Shows recently opened books that are either in progress or samples. See [Database Query](#continue-section--recent-reading-activity) for implementation details.

**Behavior**:
- Limited to ~10 most recent items
- May apply recency cutoff (observed ~7 days, needs further investigation)
- Sorted by last opened date (most recent first)

**Includes**:
- Books in progress (not finished, with reading progress > 0%)
- Recently opened samples (both cloud and downloaded)

**Excludes**:
- Finished books (shown with "Finished" + checkmark in other sections)
- Books with 0% progress (unless they are samples)

**Display format**:
- Regular books: Show actual percentage (1%-99%)
- Samples: Show "Sample" label (we ignore Apple's "1%" quirk for cloud samples)

![Continue Section - Page 1](ui/apple/Continue%20(recent)%20p1.jpg)
![Continue Section - Page 2](ui/apple/Continue%20(recent)%20p2.jpg)

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

![Previous Section - Tile View](ui/apple/Previous%20tiles.jpg)

<table>
<tr>
<td><img src="ui/apple/Previous%20list.jpg" alt="Previous Section - List View"></td>
<td><img src="ui/apple/Previous%20list%20p2.jpg" alt="Previous Section - List View Page 2"></td>
</tr>
</table>

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

#### Books Read This Year Section
Achievement-focused view showing only completed books:

![Books Read This Year](ui/apple/Books%20Read%20This%20Year.jpg)

- Attack Surface - Cory Doctorow
- Red Team Blues - Cory Doctorow
- Chip War - Chris Miller
- The Diamond Age - Neal Stephenson

**Status**: "Yearly Goal Achieved - 4 books finished. Keep reading!"

#### Series Collections
Apple Books groups books by series, showing both owned and unowned titles. Series pages can be accessed even if only one book from the series is owned. Unowned books show with price buttons:

| Hainish Series | The Baroque Cycle |
|:--------------:|:-----------------:|
| ![Series - Hainish](ui/apple/Series%20-%20Hainish.jpg) | ![Series - The Baroque Cycle](ui/apple/Series%20-%20The%20Baroque%20Cycle.jpg) |

**Working Hypothesis**: This UI suggests `ZSTATE = 5` may be associated with series entities and unowned books within a series. Unverified: a later census (2025-07-03) also observed 5 only as a *second* row for a title that already had a `ZSTATE = 3` row - consistent with the series structure but not settling it. Open until a fresh live-database re-census.

#### Want to Read Section
A list Apple Books computes rather than one the user marks. Across the observed titles its composition held as books with 0% progress plus any samples; what orders the list is unknown:

![Want to Read](ui/apple/Want%20to%20Read.jpg)

### Database to UI Mapping

#### Continue Section = Recent Reading Activity
**Database Query**:
```sql
SELECT * FROM ZBKLIBRARYASSET 
WHERE (
    (ZREADINGPROGRESS > 0 AND ZISFINISHED = 0)  -- Books in progress
    OR ZSTATE = 6                                -- Cloud samples  
    OR ZISSAMPLE = 1                             -- Downloaded samples
)
ORDER BY ZLASTOPENDATE DESC 
LIMIT 10;
```

**Note**: Apple may apply additional recency filtering beyond the LIMIT 10.

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

1. **Continue section shows active reading AND recently opened samples** (with ~7 day recency cutoff)
2. **Previous section shows reading history** (all states, sorted by last access)
3. **Cloud status affects availability** but not progress tracking
4. **Sample display quirk**: Cloud samples show fake "1%" progress, downloaded samples show "Sample" label
5. **PDF documents integrate seamlessly** with book progress tracking
6. **Finished books appear in multiple sections** (Previous + Year view, but never in Continue)
7. **Zero progress books still appear in Previous** if accessed before

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
- **Finished books**: Marked by ZISFINISHED = 1 alone - finished books have been observed below 100% progress; the converse held in the same data (ZREADINGPROGRESS = 1.0 implied ZISFINISHED = 1)
- **Sample books**: Read 0.0 progress in every observation, and are not identified by `ZISSAMPLE = 1` alone - see [Sample Book Handling](#sample-book-handling)

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

**Sample Lifecycle** (proposed mechanism - no sample's row was observed before and after being downloaded):
1. A user adds a sample to their library from the store. The book appears with `ZSTATE=6` and `ZISSAMPLE=0`. It is a "Cloud Sample" that is not yet downloaded.
2. Once the sample is opened or downloaded, the record reads `ZSTATE=1` and `ZISSAMPLE=1`, a "Local Sample".

The transition is inferred from one title's values changing between queries: "What's Our Problem?" read `ZISSAMPLE = 0` in one query and `ZSTATE = 1, ZISSAMPLE = 1` in a later one, while "Snow Crash" and "Tiny Experiments" held at `ZSTATE = 6, ZISSAMPLE = 0` across the same queries. Per-title `ZSTATE`/`ZISSAMPLE` values are therefore point-in-time observations rather than stable facts - re-run the query instead of quoting a title.

**Working Hypothesis**: Samples may not track reading progress percentage at all - `ZREADINGPROGRESS` read 0.0 for every sample observed. Supporting and complicating observations:
- A sample carried a type 3 annotation holding an `epubcfi` location in `AEAnnotation_v10312011_1727_local.sqlite`, which would let a reading position sync between devices without a progress percentage
- The UI nevertheless renders some cloud samples at 1% (see [UI Behavior Insights](#ui-behavior-insights))
- No sample's row was observed before and after reading it, so the 0.0 is not established as invariant

Sample-related queries live in [Database to UI Mapping](#database-to-ui-mapping).

## Critical Implementation Notes

- **Use glob patterns** for database discovery (filenames contain variable numbers)
- **BKLibrary.sqlite is authoritative** for reading progress, not Books.plist
- **Reading progress stored as float** (0.0 to 1.0), multiply by 100 for percentages
- **Use ZLASTOPENDATE for recency**, not `updateDate` from Books.plist
- **Apple timestamps** use 2001-01-01 as epoch, not Unix epoch
- **Database files include WAL/SHM** files (Write-Ahead Logging) - query main .sqlite file
- **Handle NULL values** gracefully in all timestamp and progress fields
- **Check ZISSAMPLE flag** to identify preview/trial books
- **ZCONTENTTYPE appears to distinguish books from PDFs** - the value mapping is unverified against a live database
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
    -   *Mapping:* `BKLibrary.sqlite` where `ZCONTENTTYPE = 1` (mapping unverified against a live database) or `ZKIND = "ebook"`.
-   **PDF:** A Portable Document Format file.
    -   *Mapping:* `BKLibrary.sqlite` where `ZCONTENTTYPE = 3` (mapping unverified against a live database) or `ZKIND = "pdf"`.
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

-   **Sample:** A preview version of a book, which can exist in a downloaded or not-downloaded state.
    -   *Mapping:* A book is considered a sample if `ZSTATE = 6` (a cloud sample not yet downloaded) OR `ZISSAMPLE = 1` (a downloaded sample). This composite check is necessary to correctly identify all sample types.
    -   *Note:* The `ZISSAMPLE` flag alone is not a reliable indicator. We have confirmed cases (e.g., "Snow Crash") where a book is a sample in the UI but has `ZISSAMPLE = 0` in the database, being identified instead by its `ZSTATE` of `6`.
-   **Cloud:** The book is stored in iCloud and not fully downloaded locally.
    -   *Mapping:* `BKLibrary.sqlite` where `ZSTATE` indicates cloud/local status.
    -   *Observed ZSTATE Mappings (2025 census - re-verify against a live database before relying on these):*
        - `ZSTATE = 3`: **Cloud Book**. The book is stored in iCloud.
        - `ZSTATE = 6`: **Cloud Sample (Not Downloaded)**. Sample added to library/wishlist but not downloaded yet. Shows in "My Samples" on Mac and "In Your Library" as Sample on iOS. Has no ZKIND, ZPATH, or reading progress until downloaded.
        - `ZSTATE = 1`: **Local Book**. The book is stored on the device. This includes:
            - Regular downloaded books
            - Downloaded samples (where `ZISSAMPLE = 1`)
            - Caveat: books showing the UI cloud icon have been observed at `ZSTATE` 1, 3, and 6. The database is per-machine while those UI observations were cross-device, so `ZSTATE = 1` may mean local-on-the-queried-machine rather than downloaded-everywhere - settle it with a same-machine census (database query beside that machine's UI).
        - `ZSTATE = 5`: **Open hypothesis - Series Entity / Unowned Series Book?** Joining on `ZSERIESID` from an owned book ("The Left Hand of Darkness", `ZSTATE = 1`) returned three rows at `ZSTATE = 5` sharing its series id: one carrying the series name ("Hainish", author "MultipleAuthors") and two carrying individual titles the library does not own ("Five Ways to Forgiveness", "The Word for World is Forest"). No criterion for telling the series row from the unowned-title rows was established - the generic author string is not one, and the title alone was never confirmed as one. The value is not rare either: one 2025 library held 206 rows at `ZSTATE = 5`, dominated by store collections and public-domain titles (Cars, Ramses, Dune, Jane Eyre). A census on 2025-07-03 observed 5 only as a *second* row for a title that already had a `ZSTATE = 3` row - consistent with the series structure but not settling it. Treat 5 as unmapped until a fresh live-database re-census.

## CLI Mapping (Proposed Commands)

This section outlines how the domain language translates into user-facing CLI commands.

-   **`bookminder list` (Default: `recent`):** Shows "In Progress" books, ordered by `ZLASTOPENDATE`, limited to 10.
-   **`bookminder list all`:** Shows all books in the library, regardless of reading status, ordered by `ZLASTOPENDATE`. (Maps to Apple Books "Previous Section").
-   **Filtering by Reading Status (`--filter` option):**
    -   `bookminder list --filter finished`
    -   `bookminder list --filter unread`
    -   `bookminder list --filter in-progress`
-   **Filtering by Content Type (`--filter` option):**
    -   `bookminder list --filter book`
    -   `bookminder list --filter pdf`
-   **Filtering by Attributes (`--filter` option):**
    -   `bookminder list --filter sample`
    -   `bookminder list --filter cloud`
    -   `bookminder list --filter !cloud` (exclude cloud books)
    -   `bookminder list --filter !sample` (exclude samples)
-   **Filtering by Time (`--year` option):**
    -   `bookminder list --year <YYYY>` (e.g., `2024`, `current`)
-   **Pagination (`--limit`, `--offset`):**
    -   `bookminder list all --limit 20`
    -   `bookminder list all --offset 20 --limit 20`