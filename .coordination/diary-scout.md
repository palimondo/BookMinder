# Diary Scout Report — `claude-dev-log-diary/`

Read-only reconnaissance, 2026-08-12. Scope: lay of the land for a possible multi-agent extraction swarm. No bulk reads performed; all findings from `ls`/`du`/`wc`/`grep`/`git log` plus small sampled windows.

## 0. Overlap verdict (headline)

**They overlap heavily.** The YAML story-card system was born at commit `8718e5e` on **2025-06-27 15:49** ("docs: Migrate TODO.md to YAML story cards and refine backlog"), and full console transcripts continue for another 16 days, ending **2025-07-12 ~22:47** (`day-021.md`, last commit `f5f6e9e`). Story-card-era development is therefore covered by **12 transcript files** (`day-010` … `day-021`) totalling **~7.3 MB / ~820k tokens** — roughly **70% of the entire diary by volume sits inside the card era.**

The migration decision itself is captured verbatim, not merely implied: `day-011.md` lines ~8985–9600 contain the user's provoking message, Gemini's proposal, the acceptance criteria rewrite, and the commit that created `stories/`. There is no gap to bridge on the near side; the gap is on the *far* side — transcripts stop on 2025-07-12 while card-driven work ran on through 2025-07-13/14 (the `validate-filter-values` and `filter-by-sample-flag` stories were marked `done` on 07-13, and the "YOLO mode retrospective" landed 07-14) with **no transcript coverage**. Gap after coverage ends: **~2 days of product work (2025-07-13 → 07-14), then a topic pivot.**

## 1. Inventory

Total `12M` / 83 files. Three classes plus a tooling sidequest.

| Class | Files | Bytes | Format & naming | Notes |
|---|---|---|---|---|
| Raw console transcripts | `day-001.md` … `day-021.md` (21) | 10.3 MB | Terminal scrollback, manually copy-pasted from the TUI. ANSI box-drawing preserved (`╭─╮`, `│`, `⏺`, `⎿`, `✦`). | The corpus. Sequential day numbering, **not** dates. |
| Gemini-produced summaries | `gemini-summary-day-NNN-NNN.md` (10) | 125 KB | XML-ish envelope: `<user>…</user>` then `<assistant model="gemini-2.5-pro-0506">…`. Prose review, not structured data. | Pairs of days (`001-003` covers three). Already-digested layer — useful as an index, unreliable as ground truth. |
| Hand-written notes | `README.md`, `moments_of_clarity.md` | 5 KB | Markdown. `moments_of_clarity.md` is a curated highlight reel of Opus reasoning excerpts, with a legend (`Oppie = Opus`, `Sonny = Sonnet`). | `README.md` documents intent for the archive incl. a "Future Vision: Intelligence System" section that anticipates exactly this swarm. |
| `tools/` (xs sidequest) | 47 files | 652 KB | `explore_session.py` (74 KB) + `specs/` + `docs/`. Internals skipped per brief. | Self-contained. Includes `specs/golden_outputs/session_1e83.txt` (158 KB) — a *derived* transcript render, not source material. |

Notable absence: `README.md` advertises `github/*.jsonl` (JSONL extracted from GitHub Actions runs). **That directory does not exist in the repo** — it is untracked/never committed. The only JSONL present is two tiny test fixtures under `tools/specs/fixtures/`. So there are **no JSONL session transcripts in the diary**; the corpus is console-scrollback only, with all the truncation that implies (`… +27 lines (ctrl+r to see all)`).

### Sub-classification of the 21 transcripts by originating agent

The corpus is not homogeneous — the tool changes under it three times, detectable from line 1 of each file:

| Files | Agent | First-line signature |
|---|---|---|
| `day-001` | none — hand-written notes | `# BookMinder Development Log - Day 1` (44 lines; an outlier, not a transcript) |
| `day-002` … `day-004` | Claude Code (research preview) | `✻ Welcome to Claude Code research preview!` |
| `day-005` … `day-010` | Claude Code (GA) | `✻ Welcome to Claude Code!` |
| `day-011` … `day-016` | **Gemini CLI** | ASCII `GEMINI` banner / `punycode` DeprecationWarning |
| `day-017` … `day-019` | Claude Code via `claude-trace` | `claude-trace` invocation line |
| `day-020`, `day-021` | Claude Code | `claude` |

This matters more than it looks: **six of the twelve overlap-era files are Gemini, not Claude.** The story-card system is a Gemini-era invention.

## 2. Time coverage

Sessions were transcribed by hand after the fact, so the reliable anchor is the commit that added each file (`[claude-dev-log-diary] day-NNN` commits), cross-checked against dates appearing inside the transcript text.

| File | Added (commit date) | In-content date evidence |
|---|---|---|
| `day-001`, `day-002` | 2025-04-17 | `Sun Apr 13 02:42:28 2025` |
| `day-003` | 2025-05-04 | — |
| `day-004`, `day-005` | 2025-05-25 | — |
| `day-006`, `day-007` | 2025-05-29 | — |
| `day-008`, `day-009` | 2025-06-23 | — |
| `day-010` | 2025-06-27 20:41 | `2025-06-26` ×9, `Fri Jun 27 02:57:46 2025` |
| `day-011` | 2025-06-27 20:45 | `2025-06-27` ×549, `Fri Jun 27 05:24:14 2025` |
| `day-012` | 2025-06-28 | — |
| `day-013` | 2025-06-30 | — |
| `day-014`, `day-015` | 2025-07-03 | — |
| `day-016`, `day-017` | 2025-07-04 | `Fri Jul 4 19:02:50 2025` |
| `day-018` | 2025-07-05 | — |
| `day-019` | 2025-07-07 | — |
| `day-020`, `day-021` | 2025-07-12 | `2025-07-07` ×43, `Sat Jul 12 18:57:29 2025` |

**Coverage span: 2025-04-13 → 2025-07-12.** Repo history itself begins 2025-03-29 (`f0bec8e` initial commit) — so the first two weeks of the project, including the authoring of `ORIGINAL_VISION.md` and `CLAUDE.md`, predate the archive.

**Coverage stops hard at 2025-07-12 22:47.** Nothing after that was ever transcribed. What follows, unwitnessed:

- **2025-07-13** (11 commits) — filter-validation TDD cycle end-to-end, two stories marked `done`.
- **2025-07-14** (4 commits) — "YOLO mode retrospective and missing acceptance tests", `cli_spec` reorganisation.
- **2025-07-21 → 08-02** (~120 commits) — topic pivot: test-directory restructuring, GitHub Actions/Claude workflow integration, then the `xs`/`explore_session` sidequest that produced `tools/`. Product development effectively stopped; tooling took over.
- **2025-10-04, 2026-01-07** — two isolated commits.
- **2026-08-10 →** — the present analysis era.

## 3. The overlap, precisely

```
2025-03-29  repo starts
2025-04-13  ┌ transcript coverage begins (day-002)
            │
2025-06-27  │ ┌ story cards born (8718e5e, 15:49)  ── captured live in day-011
            │ │
2025-07-12  └─┤ transcript coverage ENDS (day-021, 22:47)
              │
2025-07-13  ✗ │ card-era work continues UNWITNESSED (validate-filter, sample-flag → done)
2025-07-14  ✗ │ YOLO retrospective — no transcript
2025-07-21  ✗ └ pivot to tooling; product dev dormant
```

- **Overlap window: 2025-06-27 → 2025-07-12 = 16 days**, covering `day-010` through `day-021`.
- **Gap after coverage: 2 days of active card-driven product work (07-13, 07-14)**, then the era ends anyway.
- The overlap is not incidental. Story-card references are dense throughout it:

| File | `stor(y|ies)/`+`yaml`+"story card" hits | User turns |
|---|---|---|
| `day-010` | 30 | 68 |
| `day-011` | 289 | 77 |
| `day-012` | 19 | 28 |
| `day-013` | 33 | 40 |
| `day-014` | 0 | 8 |
| `day-015` | 29 | — (Gemini marker) |
| `day-016` | 76 | — (Gemini marker) |
| `day-017` | 117 | 33 |
| `day-018` | 59 | 158 |
| `day-019` | 34 | 92 |
| `day-020` | 153 | 717 |
| `day-021` | 427 | 135 |

`day-021` (the last file, 712 KB) is the densest story-card discussion in the archive. Coverage ends at peak signal, not at a natural taper.

## 4. Intent recoverability

Sampled `day-002.md` (2025-04-13, first real transcript, 195 KB / 3687 lines / 39 user turns): opening 150 lines read in full, plus an index of all user turns.

**Verdict: the dialogue carries a class of information git does not preserve at all.** Git shows *what the tree became*; the transcript shows *what was proposed, rejected, and why* — including proposals that never reached a commit and therefore left no trace anywhere else.

The opening 60 lines alone contain: a rejected `requirements.txt` (never committed, so invisible to git), a rejected `bookminder/core` + `tests/` layout, and the requirements dialogue that produced the project's actual scope. Three short illustrative utterances:

> `> I don't know yet... did you gather requirements in a dialog with me?`

— the user refusing to let the agent guess at structure; this single line is the origin of the `<requirements_gathering>` section now in `CLAUDE.md`.

> `> 1. List books, if possible by last read. I'd like to talk to LLMs like Claude about the books that I am reading on my iPhone. Then we should be able to talk about last chapter that I read. Or about new nighlight I made since we last spoke.`

— the actual product motivation, stated once, in prose, never restated in a commit message.

> `> W8!!! what are you doing in `claude-dev-log-diary`?! I store there transcripts of our session history that I manually copy from command line. You shouldn't concern` … (line 889)

— the origin of the `<file_operations>` rule "Never access `claude-dev-log-diary/` without explicit permission". A one-line guardrail in `CLAUDE.md`; here is the incident that caused it.

And from `day-011.md` line ~9018, the message that created the story-card system:

> `> w8, waht are you doing? The first scenario should be CR (was previously completed, but we are extending it. But you've marked the Better Errror Handling as [CR], but that's already completed. Our TODO list is getting unweildy... check @vision.md for a proposal how to handle stories with YAML. Let me know it that makes sense and if co, you can star using it with what we have`

The commit `8718e5e` records "Migrate TODO.md to YAML story cards and refine backlog". It does not record that the migration was triggered by status-tag confusion in a TODO list that had become unwieldy, that `vision.md` already held the proposal, or that the user asked the agent to sanity-check the idea before adopting it. All three live only here.

**Signal density estimate: high, and it rises over time.** 1,772 user turns across the corpus (`^> ` marker; Gemini files under-count — their prompts use a box-drawn `│ >` form, so `day-015`/`day-016` show 0 spuriously). `day-020` alone has 717 user turns in 291k words — roughly one user intervention per 400 words, i.e. a genuinely conversational session rather than a monologue. The user's turns are predominantly *corrective and interrogative* ("what's core? and conf?", "explain how you'd came up with these specific version numbers?", "Did you run test in RED phase?!?", "I don't want to commit the empty `__init__.py` files! Why do we have them again?") — exactly the utterances that encode design rationale.

**Swarm-processing this is very likely to recover rationale that exists nowhere else.** Specifically recoverable: the provenance of nearly every rule in `CLAUDE.md` (most were written *in response to an observed failure*, and the failure is on tape); rejected designs; the `--flag`→`--filter` rename debate; why `list-recent-books.yaml` is currently `reopened`. The `gemini-summary-*` files are a poor substitute — they are third-hand prose written for a different purpose (calibrating Gemini's communication style to the user) and they compress 195 KB into ~12 KB, discarding precisely the corrective turns that matter.

## 5. Swarm feasibility notes

**Volume.** ~882k words / **~1.18M tokens** across the 21 day files. Not single-context. Gemini summaries add ~35k tokens total and are cheap to preload as an orientation layer.

**Per-file token estimates** (words × 4/3):

| File | Tokens | | File | Tokens |
|---|---|---|---|---|
| `day-001` | 0.2k | | `day-012` | 23k |
| `day-002` | 28k | | `day-013` | 28k |
| `day-003` | 17k | | `day-014` | 7k |
| `day-004` | 43k | | `day-015` | 32k |
| `day-005` | 21k | | `day-016` | 51k |
| `day-006` | 30k | | `day-017` | 21k |
| `day-007` | 53k | | `day-018` | 60k |
| `day-008` | 33k | | `day-019` | 43k |
| `day-009` | 62k | | **`day-020`** | **388k** |
| `day-010` | 46k | | `day-021` | 94k |
| `day-011` | 96k | | | |

**Sharding.** One agent per day file is the natural unit — files are already session-scoped and self-contained. Three exceptions:

1. **`day-020` (388k tokens, 56k lines, 2.6 MB) must be split.** It is 33% of the corpus in one file and exceeds comfortable single-agent context. It appears to span multiple sessions (in-content dates range 2025-07-05 → 07-09). Shard on the `╭───╮ ✻ Welcome to Claude Code!` banner, which marks session restarts.
2. `day-011` (96k) and `day-021` (94k) are large but single-agent-feasible.
3. `day-001` is 44 lines of hand-written notes, not a transcript — give it to nobody, or fold it into the day-002 agent's context.

**Format quirks a swarm must know:**

- **Three different UIs.** Claude Code uses `⏺` for assistant turns, `⎿` for tool results, `> ` at column 0 for user input. Gemini CLI (`day-011`–`day-016`) uses `✦` for assistant, `ℹ` for system notices, and wraps *everything* — including user prompts and shell output — in full-width box-drawing frames (`│ … │`), so naive line-prefix parsing fails. A user-turn regex of `^> ` silently returns 0 on `day-015`/`day-016`.
- **Console truncation is lossy and unrecoverable.** Tool output is elided as `… +27 lines (ctrl+r to see all)`. File contents the agent read are frequently *not* in the transcript. Agents must not assume they can see what the model saw. The JSONL that would have preserved full tool I/O does not exist for these sessions (local sessions auto-purge after 30 days — `README.md` says so, and the purge already happened).
- **Box-drawing padding inflates apparent width** — Gemini frames pad to ~160 columns with trailing spaces. Whitespace-normalise before analysis or token estimates for those files skew high.
- **Multi-agent provenance in commits.** Gemini-era commits carry `Co-Authored-By: Gemini 2.5 Pro`. Useful for attributing a decision to the agent that made it.
- **Shell noise.** Gemini-era transcripts contain lines like `bash: TODO.md: command not found` — heredoc/commit-message quoting failures, not project errors. Don't mine them as signal.
- **Day numbers ≠ dates.** `day-NNN` is a session ordinal. Use the added-commit dates in §2 for chronology; several files were committed in same-day pairs.
- **`tools/specs/golden_outputs/session_1e83.txt` (158 KB) is derived output**, a render of a session by `xs`, not primary source. Excluding it avoids double-counting.
- **`xs` is available** (`./xs` at repo root) but operates on `~/.claude/projects/*.jsonl`, which are gone for this era. It cannot help read the `day-*.md` corpus.

**Recommended first shard if the swarm is scoped rather than exhaustive:** the 12 overlap-era files (`day-010`–`day-021`, ~820k tokens, `day-020` split). That range covers the story-card system's entire lifespan and holds the densest rationale, including its birth in `day-011` and its peak discussion in `day-021`.
