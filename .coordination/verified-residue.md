# Verified Residue — the stamped repair backlog

**verified_against: `d6df0c9`** (branch `claude/bookminder-recall-5ite2s`) — swept 2026-08-13. Working tree clean at sweep time; `pytest` = 53 passed.

Every claim below was extracted from a source document, converted to an executable check, and run against the tree at `d6df0c9`. Checks are inline and re-runnable from the repo root. Verdicts: **VERIFIED** (true at HEAD) / **FALSE-AT-HEAD** (true when written, since cured) / **NEVER-TRUE** (wrong even for its source time) / **UNCHECKABLE**.

## The two events that invalidate most source documents

Both source document sets — `bdd-style-canonical.md` §5 and `claude-experiments.md` "Residue at HEAD" — describe a tree that no longer exists. They were last edited 2026-08-12 16:51 and 17:43; three commits landed after them:

| Commit | Date | What it cured |
|---|---|---|
| `c09c43a` | 2026-08-12 17:46 | restored the commit-after-RED rule to CLAUDE.md; recovered SPECS_REVIEW into `.coordination/recovered/` |
| `5855069` | 2026-08-12 | replaced AGENTS.md and GEMINI.md with symlinks to CLAUDE.md — triplication drift is now structurally impossible |
| `315dce5` | 2026-08-12 18:46 | reverted the four-layer spec tree to the pre-reorg checkpoint (`c851f95`) — `specs/{unit,integration,acceptance,e2e}/` gone, concern-based layout back |

`315dce5` is the dominant event: it cured nine §5/residue items outright and **resurrected six others at new coordinates**, because the pre-reorg checkpoint it restored still carried the YOLO-era damage. Every relocated wound below is stamped with both its old citation and its coordinates at HEAD. The §5 preamble sentence "Every item verified in the working tree" is itself now FALSE — it was verified against the pre-restoration tree.

---

## 1. REPAIR BACKLOG — VERIFIED@d6df0c9

The true current defect list. Ordered code/spec first, then docs/config.

### R1 — The borrow has never been specified (§5.1)
No spec asserts that the CLI's filter vocabulary *is* the library's; `cli.py` could grow its own literal that happens to match and nothing would fail.
```
grep -rn "SUPPORTED_FILTERS is" specs/          # expect: no output
```

### R2 — Patch target still points at the CLI's imported name (§5.1, experiments Episode B) — RELOCATED
Source cited `specs/acceptance/cli_spec.py:67`; that file is gone. The mutated RED survives at **`specs/cli_spec.py:100`**.
```
sed -n '99,107p' specs/cli_spec.py            # expect: patch('bookminder.cli.SUPPORTED_FILTERS', {'foo', 'bar'})
```

### R3 — Pre-commit test comment in production code (§5.10)
```
sed -n '48p' bookminder/cli.py                # expect: # This is a test comment to trigger pre-commit hooks.
```

### R4 — Vacuous sample loops, no non-emptiness guard (§5.5) — RESURRECTED at new coordinates
Source cited `specs/integration/library_containers_spec.py:147-161`. At HEAD the same defect sits in the restored concern-based file: both sample loops are green if the filter returns nothing, while their cloud siblings eight lines above are guarded.
```
sed -n '150,162p' specs/apple_books/library_spec.py    # no `assert len(...) > 0` in either body
sed -n '134,144p' specs/apple_books/library_spec.py    # siblings DO guard (:136, :143) — the correct shape
```

### R5 — Unfalsifiable retrofit wrapper (§4(e)) — RESURRECTED by the restoration
`315dce5` brought back the `if output and "No books" not in output:` wrapper that lets the test pass while asserting nothing. This is the exact construct canonical §4(e) calls "a comment with a runtime cost".
```
sed -n '144,153p' specs/cli_spec.py           # expect line 150: if output and "No books" not in output:
```

### R6 — Near-duplicate validation specs (§5.6) — RELOCATED
Source cited `acceptance/cli_spec.py:59`/`:66`. Both now live in `describe_cli_validation`; both assert exit 1 + "Invalid filter" + "Valid filters:".
```
sed -n '91,107p' specs/cli_spec.py            # it_validates_filter_values (:92) vs …_and_shows_helpful_error (:99)
```

### R7 — `describe_bookminder_integration` names a mechanism, not a command (§5.7) — PARTIALLY RELOCATED
The `e2e/` home is gone (that half is closed, see C6); the mechanism-named block itself survived the restoration.
```
grep -n "def describe_bookminder_integration" specs/cli_spec.py    # expect: 131
```

### R8 — Duplicate `it_` and `describe_` names within and across files (§5.7) — RELOCATED
```
grep -n "def it_handles_fresh_apple_books_user_with_no_books" specs/apple_books/library_integration_spec.py   # 24, 63
grep -n "def it_excludes_samples_with_not_sample_filter" specs/apple_books/library_spec.py                    # 157, 202
grep -rn "def describe_list_all_books" specs/    # library_integration_spec.py:62 AND library_spec.py:165
```

### R9 — Error-contract asymmetry, unspecified (§5.8) — line numbers still exact
`bookminder/` was untouched by the restoration, so §5.8's citations survive verbatim.
```
sed -n '167p;171p' bookminder/apple_books/library.py
# :167 except sqlite3.Error (inside list_recent_books) ; :171 def list_all_books — no try/except
```
Related and still unexamined: `BookminderError` → exit 0 at the CLI boundary (`cli.py:82-83`, `:95-96`) while validation errors exit 1 (`cli.py:26`).

### R10 — The status ledger disagrees with itself (§5.9)
```
sed -n '13,14p;21,23p' TODO.md                # same two stories under Completed Features AND "need proper ATDD reimplementation"
grep -n "^status:" stories/discover/validate-filter-values.yaml stories/discover/filter-by-sample-flag.yaml   # both: done
```

### R11 — Dead plist API (§5.11)
`list_books` / `find_book_by_title` have zero `cli.py` callers; only specs exercise them.
```
grep -rn "list_books\|find_book_by_title" bookminder/cli.py    # expect: no output
grep -n "list_books(\|find_book_by_title(" specs/apple_books/library_spec.py   # only callers: 97, 101, 111, 118
```

### R12 — Given-supplying docstrings on implemented tests (§6, §5.10) — RELOCATED and MULTIPLIED
Source cited one survivor plus `e2e/cli_wiring_spec.py:40`. At HEAD there are eight, across two files.
```
grep -n '"""' specs/apple_books/library_integration_spec.py   # 16, 25, 30, 39, 64
grep -n '"""Integration test:' specs/cli_spec.py              # 133, 145, 156
```

### R13 — Builtin shadowing remains unsettled (§6, day-020-s1:851/:934, day-020-s2:517/:659)
`list` was renamed to avoid the clash; `format` and `filter` were not. No rule states which.
```
grep -n "def list_cmd\|^def format\|\"--filter\"\|filter: str | None" bookminder/cli.py   # :50 list_cmd ; :55 format ; :41/:73 filter
grep -n "Builtin shadowing" .coordination/bdd-style-canonical.md    # §6 still lists it open
```

### R14 — Tautological key-presence spec (day-009:437)
`it_returns_books_with_reading_progress` asserts only that three keys exist; `_row_to_book` constructs them as literals, so it cannot fail for any database contents.
```
sed -n '123,132p' specs/apple_books/library_spec.py
sed -n '69,78p' bookminder/apple_books/library.py    # the constructor the assertion restates
```

### R15 — SQL-string coupling in the `_build_books_query` spec (canonical §4, "the earlier crack")
Six assertions on the query *text* where a fixture-based behavioural alternative exists.
```
sed -n '52,73p' specs/apple_books/library_spec.py
```

### R16 — Evidence-free NULL defensiveness in the doc that taught it (day-008:340/:639) — CALIBRATION CASE, RE-VERIFIED
The miner's report was correct, and the line numbers are exact. Confirmed evidence-free by probing the fixture: zero NULL `ZISSAMPLE` rows exist anywhere in the repo.
```
sed -n '510p;561p;584p' docs/apple_books.md    # :561 = AND (ZISSAMPLE IS NULL OR ZISSAMPLE = 0)
python3 -c "import sqlite3;c=sqlite3.connect('specs/apple_books/fixtures/users/test_reader/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/BKLibrary-fixture.sqlite');print(c.execute('SELECT COUNT(*) FROM ZBKLIBRARYASSET WHERE ZISSAMPLE IS NULL').fetchone(), c.execute('SELECT DISTINCT ZISSAMPLE FROM ZBKLIBRARYASSET').fetchall())"
# expect: (0,) [(0,), (1,)]  — 6 rows, no NULLs, so the guard has never had a referent
```
Canonical §4(f) records the production-SQL twin as deleted after checking the fixtures (`library.py:163` is now `AND ZSTATE != 6 AND ZISSAMPLE != 1`). The cure was applied to the code and never to the source that taught it.

### R17 — `docs/apple_books.md` contradicts itself about its own confidence (day-008:240/:351)
```
sed -n '60p;114,115p' docs/apple_books.md     # :60 "(likely: 1 = Book, 3 = PDF)" vs :114-115 asserted flatly
```

### R18 — Python version config disagrees with itself (day-005:321) — line numbers still exact
```
sed -n '11p;71p' pyproject.toml               # requires-python = "==3.13.*" ; target-version = "py312"
```

### R19 — The formatting gate has eroded (day-005:217/:604)
`trailing-whitespace` and `end-of-file-fixer` were deleted in day-005; `ruff-format` has since been commented out entirely.
```
sed -n '15,22p' .pre-commit-config.yaml       # ruff-format commented at :21-22
grep -c "trailing-whitespace\|end-of-file-fixer" .pre-commit-config.yaml   # expect: 0
```

### R20 — CLAUDE.md mandates maintaining a `contributors` list that does not exist (day-003:391/:1024)
PEP 621 defines no such field; setuptools ignored it; the key was dropped, the rule survives.
```
grep -n "contributors" CLAUDE.md pyproject.toml    # CLAUDE.md:249-250 only — nothing in pyproject.toml
```

### R21 — README advertises unbuilt features (canonical §1, line 30)
```
sed -n '11,12p' README.md                     # "Extract table of contents from EPUB files" / "Extract highlighted passages"
grep -n "@list_cmd.command\|@main.command" bookminder/cli.py    # only: recent (:71), all (:86)
```

### R22 — CLAUDE.md:254 describes a triplication that no longer exists — NEW, found by this sweep
The instruction-synchronisation rule (day-008 provenance) tells the agent to ask whether changes should be applied to all three files. Since `5855069` they are one file. The rule is now a no-op instruction that costs a user turn every time it fires.
```
sed -n '254p' CLAUDE.md
ls -l AGENTS.md GEMINI.md                     # both: -> CLAUDE.md
git ls-files -s AGENTS.md GEMINI.md           # mode 120000 (symlink), identical blob
```

### R23 — Rule gaps at HEAD, each asserted by a miner and each confirmed absent
Six independent "no rule at HEAD" claims (day-005:280/:368, day-013:128/:167/:277/:321, day-015:188/:262/:273/:284/:350). All confirmed: CLAUDE.md contains no prohibition on `--no-verify`, no "explain before implementing" rule, no `git checkout --` restore rule, no rule against wholesale rewrites of rules files, no commit-trailer rule, and no rule against editing the fixture instead of the code.
```
grep -ci "no-verify" CLAUDE.md; grep -ci "wholesale" CLAUDE.md; grep -ci "trailer" CLAUDE.md   # expect: 0 0 0
```

### R24 — CLAUDE_REVIEW's diagnosis is unmerged and its findings still hold (experiments residue A3)
The file exists only on `origin/claude/issue-10-20250722-1917` (introduced by `3c27ecc`). Its cross-section-dependency finding is still true of HEAD: `<requirements_gathering>` directs the reader to a TODO.md structure that `<backlog_management>` does not define until 74 lines later.
```
git log --all --oneline --diff-filter=A -- CLAUDE_REVIEW.md   # 3c27ecc, off-main only
grep -n "Document requirements in the TODO.md" CLAUDE.md      # :116
grep -n "<backlog_management>" CLAUDE.md                      # :190
```

---

## 2. CLOSED — FALSE-AT-HEAD

True when written; cured since. Each names the curing event.

| # | Claim (source) | Curing event | Confirming check |
|---|---|---|---|
| C1 | `USERNAME=$1` collides with the shell's own `USERNAME` in the fixture scripts | `f4d2279` *fix: fixture scripts environment variable conflict and SQL injection* | `grep -n "FIXTURE_USER=\$1" specs/apple_books/fixtures/*.sh` → `create_fixture.sh:8`, `copy_book_to_fixture.sh:8`; `grep -c "USERNAME=" specs/apple_books/fixtures/*.sh` → 0 |
| C2 | "The four-layer taxonomy stands as if decided" (§5.3); "`specs/{unit,integration,acceptance,e2e}` split at HEAD" (canonical §2.2, line 50); whole experiments residue table | `315dce5` | `git ls-files specs/ \| grep -E "^specs/(unit\|integration\|acceptance\|e2e)/"` → no output. **Footnote:** all four directories still exist *on disk*, empty but for gitignored `__pycache__` (`git status --short --ignored specs/`). Nothing is tracked, so the taxonomy is gone from the repository — but `ls specs/` still shows it, and stale `.pyc` blobs still match unscoped greps. Worth an `rm -rf` for anyone reading the tree by eye. |
| C3 | The `__init__.py` layer contracts "claim what the contents do not meet" (§5.3) | `315dce5` | `wc -c specs/__init__.py specs/apple_books/__init__.py` → 0 and 0 (empty, per CLAUDE.md `<package_structure>`) |
| C4 | "Sample filtering has had no non-vacuous end-to-end spec since the reorg's pure move" (§5.2, experiments residue B) | `315dce5` restored the guarded fixture test | `sed -n '155,167p' specs/cli_spec.py` → `it_excludes_samples_from_recent_books` with `assert len(output) > 0` at :160 |
| C5 | `describe_bookminder_acceptance` — a block named after a layer (§5.2, §5.7, experiments residue B) | `315dce5` | `grep -rn "describe_bookminder_acceptance" --include="*.py" specs/` → no output *(scope the grep to `*.py`: stale `__pycache__` blobs still match — see the C2 footnote)* |
| C6 | `describe_bookminder_integration` lives in `e2e/` (`cli_wiring_spec.py:38`); its `:40` docstring says "Integration test:" (§5.7, §5.10) | `315dce5` | `ls specs/e2e/` → no tracked files. *(The block name itself survived — see R7; the docstrings survived — see R12.)* |
| C7 | Mechanism-suffixed `describe_list_recent_books_integration` (:117) / `describe_list_all_books_integration` (:164) (§5.7) | `315dce5` | `grep -rn "def describe_list_.*_integration" --include="*.py" specs/` → no output. *(Do not loosen to `_integration()` — that matches the surviving `describe_bookminder_integration`, R7.)* |
| C8 | Dead `TEST_HOME` at `specs/unit/library_spec.py:9` pointing into a nonexistent `specs/unit/fixtures/` (§5.10, experiments residue B) | `315dce5` | `sed -n '13p' specs/apple_books/library_spec.py` then `ls specs/apple_books/fixtures/users/test_reader` → path exists and resolves |
| C9 | `README.md:98` documents `pytest specs/apple_books/library_spec.py --spec`, "a path deleted in the reorg" (§5.10, experiments residue B) | `315dce5` — the restoration healed the doc rot by restoring the path | `ls specs/apple_books/library_spec.py` → present; the README line is now correct |
| C10 | `e2e/` reaching across into `integration/apple_books/fixtures/` (experiments residue B) | `315dce5` | `grep -rn "integration/apple_books" specs/` → no output |
| C11 | "The commit-after-RED rule is missing from the constitution. CLAUDE.md self-contradicts" (§5.4, canonical §2.6 line 87, experiments residue A1) | `c09c43a` *docs: restore commit-after-RED rule (user-approved)* | `sed -n '235,238p' CLAUDE.md` → "Make **three** distinct commits … 1. After RED phase (new failing spec, committed before implementation)" |
| C12 | "Triplication drift — AGENTS.md and GEMINI.md still carry the two-commit rule" (§5.4, experiments residue A4) | `5855069` *replace AGENTS.md and GEMINI.md with symlinks to CLAUDE.md* — cured structurally, not by editing | `git ls-files -s AGENTS.md GEMINI.md` → both mode 120000, blob `681311e` = `CLAUDE.md`. **Note: this closure creates R22.** |
| C13 | GEMINI.md's `in_review`/`completed`/`on_hold` status vocabulary diverges from CLAUDE.md's (day-013:485) | `5855069` | `grep -c "in_review\|on_hold" GEMINI.md` → 0 |
| C14 | "The reports it produced — `docs/collaboration_analysis.md`, `docs/lessons_learned.md`, `docs/claude4_collaboration_guide.md`, `docs/analysis/*` — are still in the repo and still contain the second-hand attributions" (day-006:344/:528) | `eea59e3` *docs: remove retrospective AI meta-commentary and analysis* | `ls docs/` → none of the four present; `ls docs/analysis` → no such directory |
| C15 | "The `!sample` filter was never implemented; its acceptance test remains skipped with reason 'Implement after basic list all works'" (pairing/day-019:805) | implemented pre-`d6df0c9`; no skip survives | `sed -n '162,163p;178,179p' bookminder/apple_books/library.py` → `!sample` branches present; `grep -rn "skip\|xfail" specs/*.py specs/apple_books/*.py` → no output |
| C16 | "`unit/` specifying three private functions — splitting by level left the private helpers with nowhere else to live" (experiments residue B) | `315dce5` — the *framing* is void; the helper specs live in the concern-based file by design now | `grep -n "def describe_get_user_path\|def describe_build_books_query\|def describe_row_to_book" specs/apple_books/library_spec.py` → 37, 52, 76 (in `apple_books/`, not `unit/`) |

---

## 3. NEVER-TRUE

Wrong at the time of writing, not merely stale.

**N1 — day-007:646:** "the day-007 `Books.plist` and its empty `401429854.epub` placeholder are gone."
Both files were present in the tree the miner was describing, at `specs/integration/apple_books/fixtures/users/test_reader/…`, and both are present at HEAD. The epub is still a 0-byte placeholder. The miner appears to have checked the `fixtures/` directory root rather than the per-persona user homes it had just correctly described one clause earlier.
```
git ls-tree -r --name-only 315dce5^ | grep -E "401429854.epub|test_reader.*Books.plist"   # present pre-restoration
git ls-tree -r --name-only HEAD     | grep -E "401429854.epub|test_reader.*Books.plist"   # present at HEAD
ls -l specs/apple_books/fixtures/users/test_reader/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books/401429854.epub   # 0 bytes
```

**N2 — day-007:645:** "The user asked for `/docs/fixtures.md`; the agent silently created `docs/test_fixtures.md`. Neither file exists at HEAD."
`docs/test_fixtures.md` exists at HEAD and existed at `315dce5^`. Only the `docs/fixtures.md` half is correct.
```
ls docs/test_fixtures.md          # present
ls docs/fixtures.md               # No such file — this half stands
git ls-tree HEAD docs/test_fixtures.md   # tracked
```

---

## 4. UNCHECKABLE

**U1 — pairing/day-010:457:** "the real *Tidy First?* sits at 5% and the real GOOS at 7% in the library the tool lists."
Requires macOS with the author's live Apple Books database. The repo's only real fixture is synthetic (6 rows: Extreme Programming Explained, The Left Hand of Darkness, Lao Tzu, Snow Crash, Tiny Experiments, What's Our Problem?) and contains neither title. The claim's own text flags it as circumstantial.

**U2 — day-002:8 and day-002:643:** "the `day-001.md` committed at HEAD is the agent's 44-line summary"; "the raw day-001 transcript exists nowhere else in the repository."
Existence is confirmed by index metadata (`git ls-files claude-dev-log-diary/` → `day-001.md` tracked), but the line-count and uniqueness halves require reading `claude-dev-log-diary/`, which CLAUDE.md:261 forbids without explicit user permission. Blocked by project policy, not by capability — a single user "go" converts this to checkable.

**U3 — the entire `loc:` citation layer of the mining corpus** (`day-0NN:LNNNN`, several hundred references).
Same policy block as U2. This is the corpus's largest unverified surface: the validator audits `quote:` fields for internal schema conformance, not for correspondence to the transcript lines they cite. One fabricated instance was already caught in day-018 by the repair agent, so the prior is not zero.

**U4 — day-006:528 content half:** "the reports … still contain the second-hand Freeman/Pryce/Farley attributions and the reversed framing."
The container claim is FALSE-AT-HEAD (C14 — files deleted by `eea59e3`), which makes the content claim unverifiable at HEAD rather than false. Recoverable from `eea59e3^` if it ever matters.

---

## 5. Sweep stats

**Sources swept:** 24 `mining/v2/*.yaml` + 3 `mining/pairing/*.yaml` (21,379 lines total) + `bdd-style-canonical.md` §§1-6 + `claude-experiments.md` Residue-at-HEAD × 2 and LESSONS.

**Extraction:** 114 present-tense marker hits across the 27 YAMLs (`at HEAD|still …|currently|sits at|remains|persists|never been|has never|today`), of which the large majority are source-time narrative or quoted user speech rather than repo-state assertions — the base rate of true present-tense repo claims in the corpus is roughly 1 in 4 marker hits.

**Adjudicated: 46 distinct present-tense repo-state claims.**

| Verdict | Count | Share |
|---|---|---|
| VERIFIED@`d6df0c9` | 24 | 52% |
| FALSE-AT-HEAD | 16 | 35% |
| NEVER-TRUE | 2 | 4% |
| UNCHECKABLE | 4 | 9% |

**By source:** canonical §5 — 11 items in, 5 VERIFIED (2 of them only after relocation), 6 FALSE-AT-HEAD. `claude-experiments.md` Residue-at-HEAD tables — 14 items in, 12 FALSE-AT-HEAD (the reorg residue table is now almost entirely historical). Mining YAMLs — 21 adjudicated, 17 VERIFIED, 2 NEVER-TRUE, 2 UNCHECKABLE; the miners' line-anchored config and docs claims (`pyproject.toml:11`/`:71`, `CLAUDE.md:243`/`:244`/`:254`/`:261`, `docs/apple_books.md:60`/`:114-115`/`:510`/`:561`/`:584`) were **exact** in every case checked.

**Surprises worth the coordinator's attention:**

1. **Curing an item can create one.** `5855069` closed the triplication drift (C12) and thereby made CLAUDE.md:254 a stale instruction (R22). No document noticed, because the two facts live in different files.
2. **Restoration resurrects as well as cures.** `315dce5` bought back the guarded fixture tests (C4) at the price of six wounds returning under new coordinates (R2, R4, R5, R6, R7, R8, R12) — the pre-reorg checkpoint still carried the YOLO-era damage. Anyone re-reading §5 against HEAD by *line number* would wrongly close all of them.
3. **Doc rot healed by accident.** README.md:98 (C9) became correct again without anyone editing README.md.
4. **The miners were more reliable than the synthesis documents.** Every line-anchored miner claim checked was exact; both NEVER-TRUE findings are the same miner (day-007) reasoning about directory layout from memory rather than from a listing, in the two fields that carry no `loc:` discipline — the `parked` section.
5. **The largest unverified surface is invisible to the validator.** U3: the corpus's `loc:` layer is unaudited by construction and unreachable under current policy.
