# Apple Books drift reconnaissance — meta-task brief

A read-only census of the author's real Apple Books libraries, run on his local machines, to measure how far the live schema and data have drifted from what the fixtures froze and to settle the unknowns the skill page states as unknown. Reverse-engineering research is a different beast from ATDD feature work: this is a meta task, not a story — no story card, no production code, no fixture edits during the census. Its output feeds two consumers in order: the `docs/apple_books.md` update pass, and — only if drift is actually measured — a version-handling strategy. Deciding version handling before measuring is YAGNI.

## Machines and library

- Mac mini on current macOS: the primary census target; its library carries all the data drift accumulated since the fixtures were copied.
- Intel MacBook frozen on an older macOS: the natural cross-version control — same library, older Apple Books, so a schema difference between the two machines is a version difference and nothing else.
- iCloud syncs one library across both, which is Apple's own evidence of conservative schema evolution; per-title state (ZSTATE, downloads) can still legitimately differ per machine, so record which machine every observation came from.
- Run the same census script on both and diff the two outputs before reading either in isolation.

## Read-only rules

- Quit Apple Books first, then open the database read-only: `sqlite3 "file:$DB?mode=ro"` — never write to a live database, never copy a live database into the repo (fixtures are populated only through `copy_book_to_fixture.sh`, later, by the author).
- Locate it by the production glob: `DB=$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/BKLibrary-*.sqlite)`; note if the glob matches more than one file.
- Query discipline from the skill page's B-57: named columns, never `SELECT *`; `?` placeholders for titles; ASCII-prefix `LIKE` retry before declaring a row absent; batch with `IN (...)`.
- Every result is recorded with its machine, app version, and OS version; a number without a machine label is unusable for the drift question.

## Census steps

- Versions: `sw_vers` and `mdls -name kMDItemVersion /System/Applications/Books.app` on each machine.
- Schema fingerprint: `PRAGMA user_version;` then `.tables`, then `SELECT Z_VERSION, Z_UUID FROM Z_METADATA;` and `SELECT Z_VERSION FROM Z_MODELCACHE;` if those tables exist. The fixture database carries only `ZBKLIBRARYASSET` at `user_version` 0 — no version metadata was ever captured, and that a live Core Data store carries `Z_METADATA` is itself an inference to confirm here.
- Schema diff: `sqlite3 "$DB" ".schema ZBKLIBRARYASSET"` on each machine versus the same command on `specs/apple_books/fixtures/users/test_reader/.../BKLibrary-fixture.sqlite`; also `PRAGMA table_info(ZBKLIBRARYASSET);` for a column-list diff. Any added, removed, or retyped column is drift.
- Table inventory: `SELECT name FROM sqlite_master WHERE type = 'table';` — the fixture knows one table; the live store's full inventory has never been recorded.
- ZSTATE census, DB-first: `SELECT ZSTATE, ZISSAMPLE, COUNT(*) FROM ZBKLIBRARYASSET GROUP BY ZSTATE, ZISSAMPLE ORDER BY ZSTATE, ZISSAMPLE;` — enumerate every distinct value first and characterize each afterwards, never reason UI-first from the values already known.
- Row counts: `SELECT COUNT(*) FROM ZBKLIBRARYASSET;` and per-table counts for whatever the inventory lists.
- Companion stores: confirm or refute the doc's `BCRecentlyOpenedBooksDB` (location and table `ZBCASSETREADINGSESSION`) and the AEAnnotation database under the iBooksX container's Documents directory with `.tables` and `.schema` only.

## Verification checklist

Each item names what to check, the query or command shape where known, and which skill entry or doc section the answer updates. Items are keyed by the skill page's entry ids (`.claude/skills/bookminder/references/apple-books-domain.md`).

### Unknowns the skill page states as ignorance

- B-45 ZSTATE 5: from the census, list the titles at 5 — `SELECT ZTITLE, ZAUTHOR, ZSERIESID, ZKIND FROM ZBKLIBRARYASSET WHERE ZSTATE = 5;` — then join from an owned series book: `SELECT ZTITLE, ZAUTHOR, ZSTATE FROM ZBKLIBRARYASSET WHERE ZSERIESID = (SELECT ZSERIESID FROM ZBKLIBRARYASSET WHERE ZTITLE = ? AND ZSTATE = 1);` and look for a column that separates the series-entity row from unowned member rows (candidates the fixture schema shows: `ZSERIESCONTAINER`, `ZLOCALONLYSERIESITEMSPARENT`, `ZSERIESISCLOUDONLY`). Updates B-45; doc "Series Collections" and "Observed ZSTATE Mappings".
- B-45 ZSTATE 1 semantics, the cross-device disagreement: on one machine, beside its own Books window, take a handful of titles at ZSTATE 1, 3, and 6 — `SELECT ZTITLE, ZSTATE, ZISSAMPLE FROM ZBKLIBRARYASSET WHERE ZTITLE IN (?, ?, ?);` — and record whether each shows the cloud icon there. The doc maps 1 as a local book; the record has cloud-icon books at 1, 3, and 6 from iPhone screenshots against the Mac database. A same-machine pairing settles whether 1 means local-on-this-machine. Repeat on the second machine for the same titles. Updates B-45; doc "Observed ZSTATE Mappings" (the ZSTATE = 1 caveat).
- B-46 sample lifecycle: pick a cloud sample (`ZSTATE = 6 AND ZISSAMPLE = 0`), record its row, have the author open or download it in the app, quit the app, re-query the same row. A before/after on one row is what the proposed 6/0 to 1/1 mechanism has never had. Updates B-46; doc "Sample Book Handling".
- B-48 ZCONTENTTYPE: `SELECT ZCONTENTTYPE, ZKIND, COUNT(*) FROM ZBKLIBRARYASSET GROUP BY ZCONTENTTYPE, ZKIND;` and name one known PDF's row. Updates B-48; doc "Content Type Identification" and Domain Language "Content Type".
- B-50 ZISFINISHED: `SELECT ZISFINISHED, COUNT(*), MIN(ZREADINGPROGRESS), MAX(ZREADINGPROGRESS) FROM ZBKLIBRARYASSET GROUP BY ZISFINISHED;` — does the live store use 0 or NULL for not-finished (the fixture's unfinished rows carry NULL), do finished rows exist below 1.0, does 1.0 ever appear without `ZISFINISHED = 1`. Name one finished book for the fixture's missing finished-book row. Updates B-50; doc "Progress Edge Cases" and Domain Language "Reading Status".
- B-51 ZLASTOPENDATE nulls: `SELECT COUNT(*) FROM ZBKLIBRARYASSET WHERE ZLASTOPENDATE IS NULL;` and the same with `AND ZREADINGPROGRESS > 0`. A non-zero second count means the unguarded conversion in `_row_to_book` needs a spec and a guard. Updates B-51; doc "Timestamp Edge Cases".
- B-52 sample progress and AEAnnotation position: `SELECT ZTITLE, ZSTATE, ZISSAMPLE, ZREADINGPROGRESS FROM ZBKLIBRARYASSET WHERE ZSTATE = 6 OR ZISSAMPLE = 1;` — any sample above 0.0 refutes the never-probed claim. Then in the AEAnnotation database, `.schema` first, and look for the type-3 row carrying an `epubcfi` location for a sample that has been read. Updates B-52; doc "Sample Book Handling".
- B-53 Want to Read ordering: `SELECT ZTITLE, ZCREATIONDATE, ZLASTOPENDATE, ZSTATE FROM ZBKLIBRARYASSET WHERE ZREADINGPROGRESS = 0 AND ZISFINISHED IS NOT 1;` beside the Want to Read list in the app on the same machine; check composition (unread-or-sample) and try each candidate order against the displayed order. Say "unknown" again if none fits. Updates B-53; doc "Want to Read Section".
- B-56 path column: `SELECT ZSTATE, COUNT(*), SUM(ZPATH IS NOT NULL) FROM ZBKLIBRARYASSET GROUP BY ZSTATE;` then for a few local rows, does the `ZPATH` file exist and does it match the plist `path` for the same `ZASSETID`. The fixture's local rows carry absolute paths; whether that is usable for the path-correlation debt is the question. Updates B-56; doc `ZPATH` field and "Asset ID Correlation System".
- B-41 plist incompleteness: `plutil -convert swift -o /tmp/Books.swift ~/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books/Books.plist`, then diff the set of `ZTITLE` values against the plist's `itemName` values; for each title missing from the plist, record its ZSTATE and ZKIND. Updates B-41; doc "Books.plist / Important Discovery".
- B-42 updateDate: for a few titles, compare the plist `updateDate` with the same row's `ZLASTOPENDATE` and `ZCREATIONDATE` and with the plist `releaseDate`; a publisher-revision reading predicts no correlation with reading activity. Updates B-42; doc "Key Fields" and "Timestamp Fields".

### Doc claims that had no recorded correction and await live re-verification

- ZSTATE 1/3/6 mapping: covered by the census and the ZSTATE-1 pairing above; confirm that every row at 6 has NULL `ZKIND` and `ZPATH` as the doc says. Doc "Observed ZSTATE Mappings".
- `BKPercentComplete` in the plist appears only on finished books and always at 1.0: count plist entries carrying the key and cross them with `ZISFINISHED = 1` for the same asset ids. Doc "Books.plist".
- Continue section: about ten items, a possible recency cutoff, samples included — compare the app's Continue section on the census machine with the doc's Continue query and with `python -m bookminder list recent`. Doc "Continue Section" and "Database to UI Mapping".
- The three "Database to UI Mapping" queries (Continue, Previous, Books Read This Year): run each and compare against the corresponding section in the app, same machine, same moment. Doc "Database to UI Mapping".
- Edge-case speculation: `SELECT COUNT(*) FROM ZBKLIBRARYASSET WHERE ZREADINGPROGRESS IS NULL;`, timestamps at or before zero (`WHERE ZLASTOPENDATE <= 0`), hexadecimal `ZASSETID` values, and whether the BKLibrary directory holds more than one database. Each finding either promotes a speculation to an observation or deletes it. Doc "Edge Cases and Special Considerations".
- Asset ID correlation: for a few rows, `ZASSETID` equals the plist `itemId` and the `.epub` file name. Doc "Asset ID Correlation System".
- Database lock while the app runs: attempt one read-only query with Apple Books open and record what happens. Doc "Database Performance and Access".
- User State Scenarios: on the machine that has other accounts, `sudo ls` the two container paths per account and check the four states the doc lists against what is there. Doc "User State Scenarios"; skill B-54.
- ZKIND vocabulary: `SELECT ZKIND, COUNT(*) FROM ZBKLIBRARYASSET GROUP BY ZKIND;`. Doc "Content Type Identification".
- Screenshots and Validation Test Cases: the doc's UI tables and named validation titles come from an older state of the library; re-shoot the sections on the census machine, label each image with its platform, and refresh the validation titles from the census rather than editing the old numbers in place. Doc "Validation Test Cases", "Apple Books UI Analysis".

## After the census

- Record results in a `## Results` section appended to this file, one bullet per checklist item, each with machine, versions, and the answer; unresolved items say "still unknown" rather than disappear.
- The doc update pass consumes the results: descriptive edits only, SQL stays in "Database to UI Mapping", screenshots beside claims, segmentation preserved (skill B-59). The skill page's entries update in the same pass.
- Version-handling strategy is designed only if the schema diff or the census shows drift; if the two machines agree with the fixture, the answer is "no drift measured" and nothing is built.
- New fixture states the specs need (a finished book, a 6-with-progress row if one exists) are named here for the author to copy in with `copy_book_to_fixture.sh`, in a separate, product-layer step.
