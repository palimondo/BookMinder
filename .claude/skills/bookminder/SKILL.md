---
name: bookminder
description: Project memory for the BookMinder repo — goals and history, Apple Books domain lore with honest verification status, repo geography and fixture architecture, current state and open author decisions. Load at the start of any BookMinder session and after any compaction, and consult before touching specs, fixtures, stories, docs/apple_books.md, README, or proposing any repo change.
---

# BookMinder — Project Memory

BookMinder is a CLI (heading for MCP) that reads a user's Apple Books library — macOS-only by design — built as a live experiment in whether an LLM can be a good pair programmer under strict outside-in ATDD. It is a deliberately tiny product and a process laboratory: story cards, acceptance specs, and disciplined commits are deliverables alongside the code. The production package (`bookminder/cli.py` → `bookminder/apple_books/library.py`) is small enough to read whole before any task, and the suite under `specs/` is the system's documentation (`pytest --spec`).

This skill is the project's cross-session memory — the environment has none, the repo is the only substrate. Facts here carry their WHY and their verification status; where state can rot, the page points at the command or file that holds truth instead of restating it. It deliberately substitutes for any machine-local memory the environment offers: project knowledge written into a machine-local store cannot reach other machines or cloud sessions, so never store project learnings there — durable facts belong here after the author ratifies them, and in-flight session state belongs in the repo's coordination record.

Sibling skill `tdd-bdd` carries the process discipline; this skill carries the project.

## Page map

- What the project is FOR, why Apple Books, the BookMind prehistory, burnout and the 2026 reevaluation, the benchmark ambition → `references/goals-and-history.md`
- Working in the tree: land mines (the permission-gated diary, huge fixtures), spec layout, backlog/story practice, settled CLI design decisions, fixture personas and the front-door `--user` seam, fixture data discipline, toolchain → `references/repo-geography-and-fixtures.md`
- Anything touching Apple Books data: containers, Books.plist vs BKLibrary sqlite, the Apple epoch, ZSTATE/ZISSAMPLE/ZCONTENTTYPE with verification status, the re-take-the-census reflex, query discipline, docs/apple_books.md's epistemic status → `references/apple-books-domain.md`
- Before judging or changing repo state: where truth lives, the open author decisions (dead plist API, story-status split-brain, unspecified SUPPORTED_FILTERS borrow), ledgered doc rot, the .coordination substrate → `references/current-state-and-open-decisions.md`

## Invariants that never wait for a page load

- Never enter `claude-dev-log-diary/` without the author's explicit, scoped permission — including via `git diff`/`git show`.
- Never propose features, platforms, or "improvements" the author has not asked for; scope discipline is the project's founding constraint.
- Apple Books schema claims are hypotheses until re-verified against a live database; re-take the census, never recall it.
- Declared story statuses and doc claims can lie; verify against the tree and `git log` before acting.
- Nothing an agent produces is repo rule until the author ratifies it.
