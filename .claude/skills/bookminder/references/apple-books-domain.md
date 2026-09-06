# Apple Books on disk

Read the section for any store, column, or user state before writing code or a spec that touches it. What a spec pins against the fixtures is established; what this page calls unknown is a boundary, not a gap to fill by reasoning from the UI or from prose. Open `docs/apple_books.md` only for the evidence behind a section; the map at the end names where it sits.

## What exists on disk

Apple Books keeps one library in two sandboxed containers under `~/Library/Containers/`:

- `com.apple.BKAgentService/Data/Documents/iBooks/Books/` holds `Books.plist` and the downloaded book files, one `<asset-id>.epub` per downloaded book.
- `com.apple.iBooksX/Data/Documents/BKLibrary/` holds the library database, `BKLibrary-*.sqlite`. Find it by that glob, never by literal name: the numeric segments in the file name differ per install.

The database is the library; the plist and the `.epub` files describe what has been downloaded from it. Books lazy-download from iCloud, so a library row with no `.epub` on disk is a normal row: presence on disk is a download state, never a membership test.

Two further stores exist: an AEAnnotation database holding highlights and annotations, where a sample's reading position lives as a type-3 row with an `epubcfi` location, and `BCRecentlyOpenedBooksDB`, holding reading sessions in `ZBCASSETREADINGSESSION`. Their schemas are in the doc only.

## Books.plist

The plist is a dict whose `Books` key holds a list of dicts, one per downloaded item, each carrying `itemName`, `artistName`, `path`, `updateDate`, and `itemId`, the asset id that also names its `.epub` file. It is the only store that carries a file path, so it is the entry point to a book's content.

Do not read reading state or membership from it. Its only progress field, `BKPercentComplete`, appears on finished books alone and always as 1.0, so it cannot express progress. Titles the database knows can be missing from the plist, even from a fresh copy, for a reason never established, so never infer membership or cloud status from plist absence. Do not sort or filter on `updateDate` either: its meaning is unverified, probably the publisher's revision date rather than reading activity; a sort on it was once built and removed for that reason. Take recency from the database's `ZLASTOPENDATE`.

Read the plist with `plistlib.load` on a binary-mode handle, which detects binary and XML itself; never shell out to `plutil -convert` from code. Guard for the list shape: a dict-keyed variant parses without error and yields zero books. For exploration, render a plist as Swift literals with `plutil -convert swift -o out.swift Books.plist`, far cheaper in tokens than XML.

## The BKLibrary database

The database is a Core Data store, hence the `Z` prefixes. The table that matters is `ZBKLIBRARYASSET`, one row per asset, authoritative for membership, reading state, and cloud and sample state.

Convert every timestamp column from the Apple epoch: values count seconds from 2001-01-01 UTC, not 1970, and they look like plausible Unix times, coming out about 31 years wrong if treated as such.

### Identity columns

- `ZTITLE` and `ZAUTHOR` are display strings and can be NULL. Never use `ZTITLE` as a key: one title can occupy several rows, at different ZSTATEs and even under two author strings for two editions. Handle duplicates explicitly in any title lookup, or detection becomes non-deterministic.
- `ZASSETID` is the asset id and names the `.epub` file, as `itemId` does in the plist; whether a join between the two works was never checked, which is the open path correlation under `ZPATH` below.

### Reading-state columns

- `ZREADINGPROGRESS` runs 0.0 to 1.0. A book with progress above 0 has been opened; that is what "recent" means.
- `ZLASTOPENDATE` is the recency source and sort key. It was never seen NULL on a row with progress above 0, so it needs no NULL guard; the doc's NULL-timestamp warnings are speculation, not observations. Add a guard only on live evidence and with a spec.
- `ZISFINISHED = 1`, alone, defines finished. Finished books exist below 100% progress, so never require `ZREADINGPROGRESS = 1.0`; `ZDATEFINISHED` is not a marker either, since one unfinished row at 69% carries a date in it, for a reason never established. Unfinished rows carry NULL, not 0, in `ZISFINISHED`, so a not-finished predicate written as `= 0` or `!= 1` matches nothing.

### ZSTATE

Use the mapping in force: 1 = present locally (downloaded books and downloaded samples), 3 = cloud book, 6 = cloud sample not yet downloaded. Treat 5 as unmapped: it was seen on a series entity row and on unowned member titles sharing a `ZSERIESID`, no criterion for telling those apart was established, and the population is large. Treat "which values show a cloud icon" as unsettled: cloud-icon books were seen at 1, 3, and 6, but that observation paired an iPhone screenshot with the Mac's database, where one title can legitimately differ, so 1 may mean local on the queried machine only. When you take a census, enumerate every distinct value from the database first and characterize each; never reason from the UI toward values you already know.

### Samples

A sample is `ZSTATE = 6 OR ZISSAMPLE = 1`. Never treat `ZISSAMPLE = 0` as proof of a full book: unmistakable samples carry 0 and are identifiable only by ZSTATE 6. Treat the lifecycle (a store sample enters as 6/0 and becomes 1/1 once opened) as a proposal, not an observation: it is inferred from one title flipping between queries, never from one row seen before and after. Re-run the query for any per-title value; never quote a title's state from notes.

Samples were never seen with `ZREADINGPROGRESS` above 0.0; their reading position lives in the AEAnnotation database instead. A sample filter on a progress-based recent list is therefore structurally near-empty; sample listing belongs on the library-wide list.

### Cloud: display versus filter

A book is cloud for display when `ZSTATE in (3, 6)`, so a cloud sample renders with the cloud glyph; the cloud filter matches `ZSTATE = 3` only and its negation `ZSTATE != 3`, so a cloud sample displays as cloud yet is excluded by the cloud filter. Leave the two as they disagree. The 3-only filter is where the author's revert of an unauthorized 3-or-6 widening left it, reverted for landing before approval, not because the wider predicate was ruled wrong; change neither side without his direction and a spec. The library-wide list accepts the cloud filter values and applies no cloud predicate; that is the current-state page's silent cloud filter.

### ZCONTENTTYPE

Treat the mapping as unverified: likely 1 = book (EPUB), 3 = PDF. Every row seen so far reads 1, so the PDF half is unconfirmed. Keep the doc's hedged wording; do not firm it up without a live query.

### ZPATH

Leave `path` empty on database-backed books, pending a `ZASSETID`-keyed correlation with `Books.plist`. Whether the database offers a usable path column was never checked on a live library: `ZPATH` exists, and in copied real rows it holds the absolute `.epub` path on local full books, NULL on cloud rows and on one downloaded sample, and on another downloaded sample a path into a `.DocumentRevisions-V100` versions store rather than the Books directory; do not rely on it. This is design debt the author left as a TODO; do not resolve it as a drive-by.

## What the app computes

Treat "Want to Read" as computed by Apple, not marked by the user: its observed composition is unread-or-sample, `ZREADINGPROGRESS = 0` and not finished, or a sample. Its ordering is unknown; do not reuse the recorded ZCREATIONDATE conclusion, which rests on an arithmetic error. Document observed database behavior, never inferred user intent, and write "unknown" where the mechanism is unknown.

Expect the UI's vocabulary to differ per platform and to lie a little: iPhone tiles and macOS list views use different attribute vocabularies, macOS "Complete" is a percentage rather than a status, and cloud samples render a fake "1%" progress. Document such quirks and never replicate them in code.

## What exists on a machine, by user state

macOS creates `com.apple.iBooksX` at account setup. The first launch of Apple Books creates `com.apple.BKAgentService`, `Books.plist`, and an empty-table `BKLibrary-*.sqlite` together, with no Apple ID required. An older install can carry `Books.plist` with no `BKLibrary` directory at all. A missing `BKLibrary` directory, an empty one, and a zero-byte database are three distinct states; report each distinctly. Reading another user's `~/Library` requires sudo, so a plain `--user <name>` run fails with PermissionError.

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
