# Memory architecture — two layers, one source of truth each

Author-ratified 2026-08-16. This file is the reasoning record; it exists so the split is not re-litigated when the discussion is forgotten. Reopening it means arguing against the reasons below, not rediscovering them.

## The problem it solves

This repo hosts sessions of different types: product development (ATDD pairing on the BookMinder CLI/MCP) and meta-project work (coordination, skill extraction, benchmark/eval development). Cloud sessions have no machine-local memory, and machine-local memory (the harness's native auto-memory) cannot reach other machines or cloud sessions anyway — so the repo itself is the only portable memory substrate. The risk the author named: mixing coordinator episodic state into product sessions, or letting a local session fork project memory into a machine-local store.

## The design

Memory is layered by concern, and each concern has exactly one source of truth (the repo's own maintenance principle):

- **Timeless project memory** — the `bookminder` skill: compiled facts, author-ratified, with WHY and verification status. Loaded at session start (skill description + instruction layer); router is the always-loaded index, pages swap on demand — the same index/topics architecture as native auto-memory.
- **Product episodic memory** — `TODO.md` (the head: the order is the plan) + `stories/` status fields + `git log` + `pytest --spec`. These are the ATDD process's own artifacts; no separate memory store is invented for them. The bookminder router orders the `TODO.md` read at load.
- **Meta episodic memory** — `.coordination/threads.md`, HANDOFF section as the head. Owned by the `project-coordinator` skill, which orders the head-read at session start and post-compaction. Never injected into product sessions.
- **Machine-local memory stores take nothing** — they silently fork the project's memory per machine.

## Why the split is not the bad kind of split-brain

Bad split-brain is two stores disagreeing about one concern (the story-status split-brain, B-62, is the resident example). Two stores for two different concerns, each authoritative for its layer, is separation of concerns. The failure mode to police is a fact living in both layers.

## The seam

A meta-layer ruling must land its product consequences in product files — e.g. the filter revert-and-redo ruling lives as reasoning in threads.md but as plan in `TODO.md`'s In Progress section. A dev session must never need to read threads.md to know what to build.

## Native-feature parity (why nothing more is needed)

Native auto-memory = always-loaded index head + on-demand topic files + write-when-worth-remembering, machine-local. The portable variant matches the architecture (router = index, pages = topics, per-layer episodic heads = the 200-line head-read) and is deliberately stricter on writes: nothing enters the skill without author ratification. The docs describe native memory as learnings-based, not a timestamped decision journal — so no episodic journal beyond threads.md/TODO.md was replicated.
