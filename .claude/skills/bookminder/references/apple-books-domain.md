# Apple Books on disk

Read the section for any store, column, or user state before writing code or a spec that touches it. What a spec pins against the fixtures is established; what this page calls unknown is a boundary, not a gap to fill by reasoning from the UI or from prose. Open `docs/apple_books.md` only for the evidence behind a section; the map at the end names where it sits.

## What exists on disk

Apple Books keeps one library in two sandboxed containers under `~/Library/Containers/`:

- `com.apple.BKAgentService/Data/Documents/iBooks/Books/` holds `Books.plist` and the downloaded book files, one `<asset-id>.epub` per downloaded book.
- `com.apple.iBooksX/Data/Documents/BKLibrary/` holds the library database, `BKLibrary-*.sqlite`. Find it by that glob, never by literal name: the numeric segments in the file name differ per install.

The database is the library; the plist and the `.epub` files describe what has been downloaded from it. Books lazy-download from iCloud, so a library row with no `.epub` on disk is a normal row: presence on disk is a download state, never a membership test.

Two further stores are known only second-hand. A relayed log analysis, never a live probe, traced a sample's reading position to a type-3 row holding an `epubcfi` location in an AEAnnotation database (`AEAnnotation_v10312011_1727_local.sqlite`), whose location and schema were never examined; a `BCRecentlyOpenedBooksDB` store is claimed with nothing in the record confirming or correcting it. Treat both as unmapped.

## Books.plist

The plist catalogues the BKAgentService container as a dict whose `Books` key holds a list of dicts, one per entry, each carrying `itemName`, `artistName`, `path`, `updateDate`, and `itemId`, the asset id that also names its `.epub` file. It is the store the code reads file paths from, so `list_books` and `find_book_by_title` stay in the tree as the seed of the EPUB content path (a ruling the current-state page holds).

Do not read reading state or membership from it. Its only progress field, `BKPercentComplete`, appears on finished books alone and always as 1.0, so it cannot express progress. Titles the database knows can be missing from the plist, even from a fresh copy, for a reason never established, so never infer membership or cloud status from plist absence. Do not sort or filter on `updateDate` either: its meaning is unverified, probably the publisher's revision date rather than reading activity; a `sort_by='updated'` option was removed for this reason and stays out until the field's meaning is established. Take recency from the database's `ZLASTOPENDATE`.

Read the plist with `plistlib.load` on a binary-mode handle, which detects binary and XML itself; never shell out to `plutil -convert` from code. Guard for list shape, as `library.py` does, because a dict-keyed variant parses without error and yields zero books. For exploration, render a plist as Swift literals with `plutil -convert swift -o out.swift Books.plist`, far cheaper in tokens than XML; the tracked `specs/apple_books/fixtures/Books.swift` and the untracked `All_Books*.swift` dumps are such renderings, of the fixture plist and of a real library's.

## The BKLibrary database

The database is a Core Data store, hence the `Z` prefixes; the table that matters is `ZBKLIBRARYASSET`, one row per asset, authoritative for membership, reading state, and cloud and sample state. `list recent` and `list all` read it through one query, `ZTITLE, ZAUTHOR, ZREADINGPROGRESS, ZLASTOPENDATE, ZSTATE, ZISSAMPLE` ordered by `ZLASTOPENDATE` descending; `list recent` adds `WHERE ZREADINGPROGRESS > 0` and a limit of ten, `list all` adds a sample predicate when asked and nothing otherwise.

Convert every timestamp column from the Apple epoch: values count seconds from 2001-01-01 UTC, not 1970, and they look like plausible Unix times, coming out about 31 years wrong if treated as such. Use `APPLE_EPOCH + timedelta(seconds=value)` as `library.py` does.

### Identity columns

- `ZTITLE` and `ZAUTHOR` are display strings; `_row_to_book` substitutes "Unknown" for a NULL in either. Never use `ZTITLE` as a key: one title can occupy several rows, at different ZSTATEs and even under two author strings for two editions. Handle duplicates explicitly in any title lookup, or detection becomes non-deterministic.
- `ZASSETID` is the store's asset id and names the `.epub` file, as `itemId` does in the plist; whether a join between the two works was never checked, which is the open path correlation under `ZPATH` below.

### Reading-state columns

- `ZREADINGPROGRESS` runs 0.0 to 1.0; `list recent` is `ZREADINGPROGRESS > 0`, and `_row_to_book` reports `int(value * 100)`.
- `ZLASTOPENDATE` is the recency source and the sort key. Leave its conversion unguarded: it was never seen NULL on a row with progress above 0; the doc's NULL-timestamp warnings are speculation, not observations. Add or remove a guard only on live evidence and with a spec.
- `ZISFINISHED = 1`, alone, defines finished. Finished books exist below 100% progress, so never require `ZREADINGPROGRESS = 1.0`; and `ZDATEFINISHED` is not a marker either: one fixture row carries a `ZDATEFINISHED` with `ZISFINISHED` NULL and progress at 69%, for a reason never established. Know the fixture's shape before writing a not-finished predicate: it holds no finished book, and its unfinished rows carry NULL, not 0, in `ZISFINISHED`, so `= 0` or `!= 1` matches nothing there. No spec pins finished-ness yet; the library spec's finished-book TODO is where it lands.

### ZSTATE

Use the mapping the code encodes: 1 = present locally (downloaded books and downloaded samples), 3 = cloud book, 6 = cloud sample not yet downloaded. Treat 5 as unmapped: it was seen on a series entity row and on unowned member titles sharing a `ZSERIESID`, no criterion for telling those apart was established, and the population is large. Treat "which values show a cloud icon" as unsettled: cloud-icon books were seen at 1, 3, and 6, but that observation paired an iPhone screenshot with the Mac's database, where one title can legitimately differ, so 1 may mean local on the queried machine only. When you take a census, enumerate every distinct value from the database first and characterize each; never reason from the UI toward values you already know.

### Samples

`is_sample` is `ZSTATE = 6 OR ZISSAMPLE = 1`, and the `_row_to_book` spec pins both halves. Never treat `ZISSAMPLE = 0` as proof of a full book: unmistakable samples carry 0 and are identifiable only by ZSTATE 6. Treat the lifecycle (a store sample enters as 6/0 and becomes 1/1 once opened) as a proposal, not an observation: it is inferred from one title flipping between queries, never from one row seen before and after. Re-run the query for any per-title value; never quote a title's state from notes.

Put sample listing on `list all`, not `list recent`. Samples were never seen with `ZREADINGPROGRESS` above 0.0, and a sample's reading position was traced to the AEAnnotation database instead; both facts are second-hand, from the relayed analysis above. Because `list recent` filters on `ZREADINGPROGRESS > 0`, a sample filter there is structurally near-empty, and its spec asserts nothing about count, so it passes on an empty result. The `list all` sample spec pins the filter against the fixture's three sample titles.

### Cloud: display versus filter

`is_cloud` is `ZSTATE in (3, 6)`, pinned by the same `_row_to_book` spec, so a cloud sample renders with the cloud glyph; but `--filter cloud` on `list recent` matches `ZSTATE = 3` only and `!cloud` matches `ZSTATE != 3`, so a cloud sample displays as cloud yet is excluded by the cloud filter. Leave the two as they disagree. The 3-only filter is where the author's revert of an unauthorized 3-or-6 widening left it, reverted for landing before approval, not because the wider predicate was ruled wrong; change neither side without his direction and a spec. Know what the specs pin: only that filtered rows are cloud, not the predicate's width, and the `!cloud` spec passes only because no fixture row sits at ZSTATE 6 with progress. `list all` accepts the cloud values and applies no cloud predicate; that is the current-state page's silent cloud filter.

### ZCONTENTTYPE

Treat the mapping as unverified: likely 1 = book (EPUB), 3 = PDF. Every fixture row reads 1, so the fixtures cannot confirm the PDF half, and no spec pins either. Keep the doc's hedged wording; do not firm it up without a live query.

### ZPATH

Leave `path` empty on database-backed books. `_row_to_book` sets `path=""` pending a `ZASSETID`-keyed correlation with `Books.plist`, and `path` is `NotRequired` on `Book` for the same reason. Whether the database offers a usable path column was never checked on a live library: `ZPATH` exists, and in the fixture it holds the absolute `.epub` path on the two local full books, NULL on the cloud rows and on one downloaded sample, and on the other downloaded sample a path into a `.DocumentRevisions-V100` versions store rather than the Books directory; do not rely on it. This is design debt the author left as a TODO; do not resolve it as a drive-by.

## What the app computes

Treat "Want to Read" as computed by Apple, not marked by the user: its observed composition is unread-or-sample, `ZREADINGPROGRESS = 0` and not finished, or a sample. Its ordering is unknown; do not reuse the recorded ZCREATIONDATE conclusion, which rests on an arithmetic error. Document observed database behavior, never inferred user intent, and write "unknown" where the mechanism is unknown.

Expect the UI's vocabulary to differ per platform and to lie a little: iPhone tiles and macOS list views use different attribute vocabularies, macOS "Complete" is a percentage rather than a status, and cloud samples render a fake "1%" progress. Document such quirks and never replicate them in code.

## What exists on a machine, by user state

macOS creates `com.apple.iBooksX` at account setup; the first launch of Apple Books creates `com.apple.BKAgentService`, `Books.plist`, and an empty-table `BKLibrary-*.sqlite` together, with no Apple ID required; an older install can carry `Books.plist` with no `BKLibrary` directory at all. The fixture personas encode exactly these states, and `library.py` distinguishes them: a missing `BKLibrary` directory raises "BKLibrary directory not found", an empty one raises "No BKLibrary database found in:", and a zero-byte database surfaces from `list recent` as "Error reading Apple Books database:"; keep all three paths specced. Reading another user's `~/Library` requires sudo, so a plain `--user <name>` run fails with PermissionError.

## Working the database

Answer one-off questions with the `sqlite3` CLI directly: no throwaway scripts in the tree, no print-debugging through production code. Name columns, never `SELECT *`, because blurb columns flood the context. Pass titles as `?` parameters; hand-escaping apostrophes fails repeatedly. When a title with diacritics returns nothing, retry `LIKE` on its longest ASCII-only prefix before concluding the row is absent, because the shell round-trip, not the database, is what fails. Probe several items of one shape with a single `IN (...)`.

## Reading docs/apple_books.md

It is the research spike's territory map, re-aligned with the project's recorded corrections where the record allowed. Read "Edge Cases and Special Considerations" and "UI Behavior Insights" as guesses written in the observational voice; read the rest as the observations this page compresses. Where this page and the doc differ, follow this page. Verify an attribute against a screenshot and a live query, never against the doc's prose alone.

## Editing docs/apple_books.md

Keep it descriptive of storage: no SQL that prescribes a feature's filtering strategy. Keep every SQL query in the single "Database to UI Mapping" section and link to it from elsewhere; two copies of one query is how the doc came to contradict itself. Commit screenshots under `docs/ui/apple/` and reference each beside the claim it supports, labelled with the platform that produced it, because the platforms' vocabularies differ. Preserve the existing segmentation when updating contents.

## Further reading in `docs/apple_books.md`

- "Container Directories", "Data Sources", "Recently Opened Books Database": What exists on disk
- "Books.plist" with its "Important Discovery", "Progress Data Sources Hierarchy": Books.plist
- "Apple Timestamp Format Details": The BKLibrary database
- "BKLibrary SQLite Database" field list, with the duplicate-editions iPhone screenshot: Identity columns
- "Progress Edge Cases", "Timestamp Edge Cases": Reading-state columns
- "Observed ZSTATE Mappings" under Domain Language, "Series Collections": ZSTATE
- "Sample Book Handling": Samples
- "Content Type Identification", Domain Language "Content Type": ZCONTENTTYPE
- "Asset ID Correlation System", the `ZPATH` field: ZPATH
- "Want to Read Section", "Database to UI Mapping", "UI Behavior Insights": What the app computes
- "User State Scenarios": What exists on a machine, by user state
