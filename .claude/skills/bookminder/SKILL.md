---
name: bookminder
description: Project memory for the BookMinder repo — goals and history, Apple Books domain facts with what is established and what is unknown, repo geography and fixture architecture, current state and open author decisions. Load at the start of any BookMinder session and after any compaction, and consult before touching specs, fixtures, stories, docs/apple_books.md, README, or proposing any repo change.
---

# BookMinder — Project Memory

Work on BookMinder as a CLI (heading for MCP) that reads a user's Apple Books library, macOS-only by design, and as a live experiment in whether an LLM can be a good pair programmer under strict outside-in ATDD. Treat story cards, acceptance specs, and disciplined commits as deliverables alongside the code: the product is deliberately tiny, and the project is a process laboratory. Read the production package whole before any task, `bookminder/cli.py` → `bookminder/apple_books/library.py`, and read the system's documentation from the suite under `specs/` with `pytest --spec`.

Load this skill at the start of every BookMinder session and again after any compaction; it is the project's cross-session memory, and the repo is the only substrate that carries anything across sessions. Then read `TODO.md`, the product's episodic head: the order is the plan, and status truth is in the `stories/` cards. Take facts from the pages below, each carrying its WHY and stating as unknown what was never established; where state can rot, a page points at the command or file that holds truth, so run that command or read that file instead of trusting a restatement. Never store project learnings in a machine-local memory store: knowledge written there cannot reach other machines or cloud sessions, and this skill deliberately substitutes for it. Write by layer, one source of truth per concern: this skill holds only compiled facts the author has ratified; a meta-session's episodic head (coordination, benchmark work) is owned by that session type's own skill and record, and never mixes into product-development sessions.

Load the sibling skill `tdd-bdd` for the process discipline; this skill carries the project.

## Page map

- What the project is FOR, why Apple Books, the BookMind prehistory, burnout and the 2026 reevaluation, the benchmark ambition → `references/goals-and-history.md`
- Working in the tree: land mines (the permission-gated diary, huge fixtures), spec layout, backlog/story practice, settled CLI design decisions, fixture personas and the front-door `--user` seam, fixture data discipline, toolchain → `references/repo-geography-and-fixtures.md`
- Anything touching Apple Books data: what exists on disk (the two containers, the plist, the BKLibrary database, the stores known only second-hand), what each store is authoritative for and when to read which, the library table's columns with the predicates the code encodes and what stays unknown (ZSTATE, samples, the cloud display-vs-filter divergence, finished-ness, ZPATH), what the app computes, the machine's user states, query discipline, and how to read and edit docs/apple_books.md → `references/apple-books-domain.md`
- Before judging or changing repo state: where truth lives, settled rulings (the plist-API seed, the reopened filters), the open author decisions (the unspecified SUPPORTED_FILTERS borrow, the silent list-all cloud filter), repair practice, the .coordination substrate → `references/current-state-and-open-decisions.md`

## Invariants that never wait for a page load

- Never enter `claude-dev-log-diary/` without the author's explicit, scoped permission — including via `git diff`/`git show`.
- Never propose features, platforms, or "improvements" the author has not asked for; scope discipline is the project's founding constraint.
- Schema truth lives in the specs: what a spec pins against the fixtures is established, and a claim no spec pins is exploration residue, not knowledge. Go to a live library only on drift — a real library breaking what the suite says works, or a new Apple Books or macOS release — or when a story needs a state the fixtures do not hold.
- Nothing an agent produces is repo rule until the author ratifies it.
