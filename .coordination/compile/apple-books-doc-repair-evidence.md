# Evidence record — docs/apple_books.md repair batch

Ephemeral review aid: this file exists so the author can audit one batch of doc edits against their evidence, and is retired once consumed.

Gate applied: an edit landed only where the session record shows a claim from the initial 2025 reverse-engineering research being corrected, or shows the claim's real (second-hand, never-probed) provenance. No live Apple Books database exists in this environment, so nothing was "fixed" from reasoning alone. Trust order: skill page `.claude/skills/bookminder/references/apple-books-domain.md` (B-40..B-53) > `.coordination/compile/rule-index-bookminder.md` > `.coordination/mining/v2/*.yaml` (only `quote:` fields are validator-verified; transcript windows read for verification of the rest).

## Edits (14)

### 1. Books.plist — Key Fields: updateDate
- Was: "`updateDate`: Last modification date"
- Now: timestamp of unestablished meaning — probably the publisher's revision date, not reading activity
- Evidence: d007-R17, user-verbatim (day-007:L2708-L2711): "it's probably related to Book's revision, when the publisher pushes a new version no Apple Books? I think when working with BookMinder, we would focus on user's interactions with the book." Skill B-41: author's hypothesis, never verified — doc had it as flat fact.

### 2. Books.plist — Important Discovery: completeness
- Was: "Contains all books in library (179 total in test case)"
- Now: NOT a complete catalog — DB-known titles were missing even from a fresh snapshot, cause never established; plist absence proves nothing about membership or cloud status (counts kept on the next bullet)
- Evidence: d013-R18, d012-R14; author-verbatim (day-013:L871-L872): "So why the \"Lao Tzu: Tao Te Ching\" is not in the All_Books.swift file (even the freshly converted one) is still a mystery to us." Fresh-conversion step day-013:L848-L860. Skill B-41.

### 3. BKLibrary — Critical Fields: ZTITLE
- Was: "`ZTITLE`: Book title"
- Now: adds "not a unique key" — one title in several rows, different ZSTATEs, once under two author strings
- Evidence: d014-R4; census day-014:L735-L764 (Attack Surface at ZSTATE 3 and 5; A Clockwork Orange under two author strings). Skill B-46.

### 4. BKLibrary — Additional Fields: ZISSAMPLE
- Was: "1 = sample, 0 = full book"
- Now: 1 = downloaded sample; 0 does NOT mean not-a-sample — see Sample Book Handling
- Evidence: d012-R13, user-verbatim (day-012:L2975): "Snowcrash is a Book Sample, as is Tiny Experiments" — both read ZISSAMPLE = 0 live. Skill B-44 (composite predicate, verified@tree).

### 5. Content Type Identification: ZISSAMPLE line
- Was: "`ZISSAMPLE = 1`: Sample/preview books"
- Now: downloaded samples — the flag alone does not identify samples
- Evidence: d012-R13 as above; d018-R16, user-verbatim (day-018:L2198): "Why do you insist on ZISSAMPLE=1? That's edge case. We want books with ZSTATE=6! (Actually we need both scenarios…)".

### 6. Timestamp Fields: updateDate
- Was: "Last modification (ISO format)"
- Now: ISO-format, probably publisher revision date, not reading activity
- Evidence: d007-R17; consistency with edit 1 so the doc does not contradict itself.

### 7. Want to Read Section
- Was: "Books displayed for future reading. Appears to be composed of books with 0% progress and any samples"
- Now: a list Apple computes, not user-marked; composition held as 0%-progress + samples across observed titles; ordering unknown
- Evidence: d018-R22, user-verbatim (day-018:L6120): "the books in Want to read aren[']t marked (this implies to me some kind of specific action by user) -- they are somehow computed, the details of that algorithm we haven't yet reverse engineered." d015-R8, user-verbatim: "We should try to find out what orders them into this list." Skill B-48.

### 8. Progress Edge Cases: finished books
- Was: "Always show ZREADINGPROGRESS = 1.0 AND ZISFINISHED = 1"
- Now: ZISFINISHED = 1 alone marks finished — observed below 100%; converse held (1.0 implied finished)
- Evidence: d011-R18; correction at day-011:L7647-L7655 ("Your findings directly contradict our previous assumption… `ZISFINISHED = 1` does NOT necessarily mean `ZREADINGPROGRESS = 1.0`… the converse holds"). Doc already carried the corrected form in Reading Status and contradicted it here. Skill B-46.

### 9. Progress Edge Cases: samples
- Was: "Can have partial progress but remain samples (ZISSAMPLE = 1)"
- Now: read 0.0 in every observation; not identified by the flag alone — see Sample Book Handling
- Evidence: d012-R13; d019-R17 (0.0 for samples); fixture corroboration day-019:L1544-L1545 ("ALL have 0% progress"). Skill B-44, B-47.

### 10. Sample Book Handling: lifecycle
- Was: flat two-step lifecycle stated as fact
- Now: same steps as "(proposed mechanism — no sample's row was observed before and after being downloaded)", with the observations it rests on ("What's Our Problem?" flipped between queries; Snow Crash and Tiny Experiments held at 6/0); per-title values are point-in-time — re-run the query
- Evidence: d019-R16 — the lifecycle text entered the doc from a document-review proposal (day-019:L963-L978) with no probe. Observed flip day-014:L480-L486; stability day-014:L495-L512. Skill B-44; ledger L-20.

### 11. Sample Book Handling: sample progress
- Was: "**Important Discovery**: Samples do NOT track reading progress percentage" + three supporting bullets
- Now: "**Working Hypothesis**: samples may not track progress — 0.0 in every observed row", with the epubcfi annotation as support, the UI-1% rendering as complication, and an explicit no-before/after-probe note
- Evidence: d019-R17 (relayed log summary, day-019:L840-L844 — no live probe); counter-observation day-019:L1616-L1617 ("The UI shows some samples with minimal progress, like \"Tiny Experiments\" at 1%"). Annotation probe day-018:L2457-L2466. Skill B-47: both claims second-hand.

### 12. Critical Implementation Notes: ZCONTENTTYPE
- Was: "**Use ZCONTENTTYPE** to distinguish between books and PDFs"
- Now: "appears to distinguish" — value mapping unverified against a live database
- Evidence: ledger L-12 ruling (contradiction-ledger.md:16, :132-:139): hedged-until-reverified stands; day-008 corpus flag (doc contradicting itself about its own confidence). Skill B-45: the hedged form governs.

### 13. Domain Language — Content Type mappings
- Was: "`ZCONTENTTYPE = 1` or `ZKIND = \"ebook\"`" / "= 3 or pdf" (flat)
- Now: same mappings with "(mapping unverified against a live database)" on the ZCONTENTTYPE half; ZKIND untouched
- Evidence: ledger L-12; the earlier pass hedged Content Type Identification only, leaving these flat. Skill B-45.

### 14. Domain Language — ZSTATE = 5
- Was: entity/member discriminator by ZTITLE (series-name vs book-title), "a later census (2025-07-03)"
- Now: the observed ZSERIESID join result stated instead (series row "Hainish"/"MultipleAuthors" + unowned titles sharing the owned book's series id), explicit "no discriminating criterion established", population scale (206 rows, store collections + public-domain), and "A census on 2025-07-03" without the ordering word
- Evidence: d015-R7, user-verbatim (day-015:L2084-L2085): "I don't think that's the correct differentiation criteria, it must be something with the entries and seriesid, the Multiple Authors is definitely a red herring" — the ZTITLE substitute was then written into the doc (day-015:L2092-L2108) with no probe. Join rows day-015:L1708-L1715; count day-015:L1536-L1541; population day-011:L7422-L7440. Skill B-43; rule-index B-43 carries the chronology fix (duplicate-row census PRECEDES the join — "later" dropped).

## NO-EDIT (16)

- Content Type Identification ZCONTENTTYPE 1/3 — already hedged by the earlier pass (b06c722).
- Series Collections ZSTATE-5 hypothesis — re-hedged by b06c722; its "later census" is correct there (post-dates the screenshots it qualifies).
- "Observed ZSTATE Mappings (2025 census — re-verify…)" heading — the over-claiming "Verified" heading was already fixed (b06c722).
- Domain Language sample composite predicate + Snow Crash note — matches skill B-44 (verified@tree); the example held stable across re-queries (day-014:L495-L500); the time-varying caveat lives once, in Sample Book Handling.
- Reading Status "Finished" note — is itself the corrected form (day-011:L7670-L7675).
- ZSTATE 1/3/6 mappings — no recorded correction; stamped needs-live-DB (B-43); section already says re-verify.
- BKPercentComplete counts (22 of 179, all 1.0) — corroborated by d009-R20.
- ZPATH field / path correlation — never actually checked (B-51); stays for the live recon.
- Apple epoch, WAL/SHM, glob discovery — verified elsewhere (B-40, B-42); doc agrees.
- User State Scenarios — matches B-49 (observed on real machines).
- Continue section behaviour — UI observation carrying its own hedge; nothing corrects it.
- Database-to-UI Mapping SQL + Sample Handling SQL — no recorded claim correction.
- Content Filtering Strategies SQL — filtering-strategy SQL outside the single mapping section, against the doc's own editing rules, but relocation/deletion is structural with no evidence gate — FLAGGED FOR AUTHOR, not executed.
- Edge Cases NULL/mixed/corrupted/timestamp speculation — B-53 marks these speculation, but no specific claim has a recorded correction; waits for the recon.
- Asset ID Correlation System — nothing in the corpus revisits it.
- UI tables, screenshots, Validation Test Cases — screenshots are the verification substrate, not the thing to edit (B-53).

## Doc vs skill disagreement — reported, not edited

- Topic: which ZSTATE values carry a UI cloud icon.
- Doc: ZSTATE = 1 is "Local Book. The book is stored on the device."
- Skill B-43: cloud-icon books observed at ZSTATE 1, 3, and 6.
- Why no edit: the observations are cross-device — doc UI tables come from iPhone screenshots, censuses ran on the Mac mini, and the same title can legitimately be local on one machine and cloud on the other (the author's own point, day-013:L822-L823). No corpus evidence resolves it; a live single-machine re-census would.
