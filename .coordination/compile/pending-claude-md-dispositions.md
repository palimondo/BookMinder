# Dispositions: claude-md-targeted rules (gardening pass)

Input: `.coordination/compile/pending-claude-md.md` (95 rules, skill_target: claude-md). Method: full corpus entry pulled per rule via `.coordination/tools/rule.py`; dispositions apply the thin-CLAUDE.md ruling (a rule earns a CLAUDE.md line only if it must bind every agent in every session), ratified provenance ranks (user-verbatim > paraphrase > synthesis; later-user-overrides-earlier), single-ownership per ledger L-07, and the 2026-08-14 commit-after-RED retirement cascade (threads.md "COMMIT-AFTER-RED RETIRED"). Repo facts verified at HEAD: PreToolUse hook `.claude/validate_git_commands.py` blocks `git add .`/`-A`/`--all` (NOT `-u`); `.pre-commit-config.yaml` excludes `claude-dev-log-diary/`; pyproject records model contributors under the `authors` key (CLAUDE.md says "contributors" — naming mismatch, flagged); `target-version = "py312"` still contradicts the 3.13 pin (pyproject.toml:71 vs :11).

## Summary

| disposition | rules |
|---|---|
| amend | 27 (consolidated into 10 drafted lines A1-A10) |
| already-covered | 41 |
| reroute | 19 (tdd-bdd 11, project-coordinator 5, bookminder 2, pair-programming 1) |
| reject | 8 |
| **total** | **95** |

Amend-list note: 27 rules collapse into 10 one-line amendments because the corpus repeats the same taught-many-times sharpenings (commit-message truthfulness x6, diary grant scoping x5, bulk-staging variants x4, constitution-editing meta-rules x6); every amendment sharpens an existing bullet in an existing section — no new sections. All drafts are written against section names, not exact line text, because a sibling worker is concurrently reverting the commit-grammar lines in `<tdd_discipline>`/`<git_workflow>`; apply these against its result.

## Amend — drafted lines

- **A1** → `<git_workflow>`, replace the existing `git add .` bullet with: "Never use `git add .`, `git add -A`/`--all`, or `git add -u` - always stage files explicitly by name; the PreToolUse hook (.claude/validate_git_commands.py) blocks bulk staging and must never be worked around." (Follow-up for author: the hook does not yet block `-u` — d020s5-R10 says it should.)
- **A2** → `<git_workflow>`, add: "A commit message may claim only what the staged diff actually does: verify it against the diff, never attribute a benefit the change does not deliver, drop references to work-in-progress states the reader cannot see, and state the why without 'This commit...' preamble or filename inventories."
- **A3** → `<file_operations>`, add beside the `git mv` bullet: "Remove tracked files with `git rm`, never plain `rm`, so the removal is staged and visible."
- **A4** → `<file_operations>`, extend the claude-dev-log-diary bullet with: "...without first asking for explicit user permission; a grant is scoped to the exact file (and line range) named in it — never load a day-0NN.md in full; search with ripgrep or read the paired gemini-summary first."
- **A5** → `<file_operations>`, add: "Write project documents in plain markdown with word markers such as [COMPLETED] — no emoji status decoration in TODO.md, docs/, or commit bodies — and keep bash blocks in docs comment-free and copy-pasteable, with explanation in the surrounding prose."
- **A6** → `<project_maintenance>`, replace "Update the contributors list whenever Claude is upgraded to a newer version" with: "Append to the contributors list whenever the acting model changes; never replace or remove a past contributor." (Note for author: the pyproject key is `authors`, CLAUDE.md says "contributors" — align the wording.)
- **A7** → `<project_maintenance>`, add: "Never change the package version as a side effect of other work; a version bump is a separate decision with its own reason and commit."
- **A8** → `<project_maintenance>`, add: "CLAUDE.md is the single canonical rules file: never create a parallel principles document, and add a new rule by extending the section that already owns its concern, as a targeted edit against the current text — never a whole-file rewrite."
- **A9** → `<project_maintenance>`, add: "When consolidating or removing rules text, enumerate every line it contained and show where each one lands before committing; a deletion may never ride along unshown."
- **A10** → `<backlog_management>`, add: "Record deferred work as a pinned entry at the top of TODO.md at the moment of deferral; never delete, demote, or renumber an existing entry while editing the file for another purpose."

| rule_id | rule gist | disposition detail |
|---|---|---|
| d019-R23 | git add prohibition mechanized as hook | amend A1 — hook exists at HEAD; the constitution should name it so no agent works around it |
| d020s1-R22 | stage by name; hook blocks bulk adds | amend A1 |
| d020s5-R10 | never `git add -u` either | amend A1 — `-u` is the variant the hook misses; named in the drafted line |
| d021-R24 | bulk adds blocked, must not be worked around | amend A1 — "must never be worked around" clause |
| d002-R19 | message must describe the change actually made | amend A2 |
| d005-R10 | write message against the diff the reader sees | amend A2 |
| d007-R14 | never claim a benefit the diff doesn't deliver | amend A2 — user-verbatim, needed-enforcement |
| d009-R17 | named capability must point at delivering code | amend A2 |
| d013-R12 | delete sentences about unstaged files | amend A2 |
| d016-R11 | benefit-stating body, no preamble/file inventory | amend A2 — partially covered by existing "not just what files were modified" bullet; drafted line completes it |
| d018-R19 | `git rm` not `rm` for tracked removals | amend A3 — `<file_operations>` names only `git mv` at HEAD |
| d013-R5 | diary grant scoped to exact file+range | amend A4 |
| d014-R9 | diary per-request per-range, cite what you learned | amend A4 |
| d015-R14 | diary grant per-file, stated purpose only | amend A4 — taught repeatedly across 3+ sessions |
| d020s1-R24 | never load day file in full; rg or summary first | amend A4 — context-destruction guard, binds every session |
| d020s3-R18 | diary permission + restate constraints first | amend A4 — restate-constraints nuance carried by scoping clause |
| d009-R18 | plain markdown word markers, no emoji decoration | amend A5 — user-verbatim, needed-enforcement, nothing at HEAD covers it |
| d009-R19 | no comments in doc bash blocks, copy-pasteable | amend A5 |
| d006-R10 | append contributors, never replace | amend A6 — entry's own feasibility note: current "Update" wording was read as overwrite; one-word-class fix |
| d006-R11 | no version bump as maintenance side effect | amend A7 |
| d002-R8 | single canonical CLAUDE.md, no parallel docs | amend A8 |
| d008-R4 | new rule joins the owning section | amend A8 |
| d013-R9 | amend rules files by targeted edit, never whole-file write | amend A8 |
| d021-R23 | search for the owning section before adding one | amend A8 |
| d002-R9 | item-by-item verification when merging rules docs | amend A9 |
| d008-R5 | removal plans enumerate where every line lands | amend A9 |
| d005-R17 | pinned deferral entries at top of TODO.md, never demoted | amend A10 — enforcement clause `<session_workflow>`'s "living document" line lacks |

## Already-covered

| rule_id | rule gist | covered where |
|---|---|---|
| d002-R17 | empty `__init__.py`; configure linter not files | CLAUDE.md `<package_structure>` (Empty __init__.py Files + Avoid Boilerplate) |
| d003-R2 | run hooks, re-stage modified files, commit | CLAUDE.md `<git_workflow>` "Stage all files after running pre-commit hooks that modify files" — this session is the line's verified origin |
| d003-R6 | never `git add .`; name every path | CLAUDE.md `<git_workflow>` (base rule; sharpenings go to A1) |
| d003-R7 | move, never copy; delete source same turn | CLAUDE.md `<file_operations>` "Always use `git mv` for moving files" |
| d003-R8 | config files free of explanatory comments | CLAUDE.md `<code_style>` "NEVER add redundant comments" + `<anti-patterns>`; entry itself confirms rule predated the incident |
| d003-R14 | record acting model in pyproject contributors | CLAUDE.md `<project_maintenance>`; NOTE for author: pyproject's key is `authors` (live, append-style at HEAD), CLAUDE.md says "contributors" — see A6 note |
| d004-R10 | `git mv`, never read+write or mv+git rm | CLAUDE.md `<file_operations>` |
| d004-R12 | docs in docs/, lowercase filenames, no root SHOUTING_FILES | CLAUDE.md `<file_operations>` "Place documentation in docs/ directory" |
| d004-R13 | no comment restating the line beneath | CLAUDE.md `<code_style>` |
| d004-R20 | stage explicitly by name | CLAUDE.md `<git_workflow>` |
| d005-R3 | never `--no-verify`; fix hook, prove via hook | tdd-bdd T-28 (cycle-and-commits.md: "Never bypass a failing quality gate (skip flags, no-verify...)") |
| d005-R11 | never `git add .`/`-A` in this repo | CLAUDE.md `<git_workflow>` — this session is the line's provenance |
| d005-R12 | exclude specs/ from mypy, keep ruff | tdd-bdd T-45 (writing-a-spec.md) + config in force at HEAD (.pre-commit-config.yaml:31) |
| d005-R18 | order backlog by dependency before committing | CLAUDE.md `<backlog_management>` "Implementation order in TODO.md should reflect natural feature progression and dependencies" — this session is its provenance |
| d007-R12 | one-line docstrings public, none private, no NumPy blocks | CLAUDE.md `<code_style>` Documentation ("Minimal, focused docstrings for complex functions only") |
| d007-R20 | delete orphaned comment when linter deletes its line | CLAUDE.md `<code_style>` "NEVER add redundant comments" — the orphan case is the same rule applied over time |
| d008-R3 | ask the human for a rule's actual rationale, never invent one | pair-programming P-09 (own your conclusions, never attribute what was not said) + ratified because_source provenance ranks in the compile policy |
| d008-R15 | never cite a rule you have not located; quote the section | pair-programming P-10 ("Quote what you read... read it in that turn and cite the line") |
| d010-R13 | stage explicitly by name | CLAUDE.md `<git_workflow>` |
| d010-R14 | `git mv`; on "destination exists" inspect both, never rm the tracked one | CLAUDE.md `<file_operations>` (core); the destination-exists nuance is minor enough to leave to the file's rule |
| d010-R15 | mirror CLAUDE.md rules into AGENTS.md/GEMINI.md | CLAUDE.md `<project_maintenance>` final bullet — current ratified form is ask-the-user, which supersedes same-commit automation (later-overrides-earlier) |
| d010-R16 | /expert-council convenes the TDD/BDD gurus | pair-programming council.md (P-29..P-39, grounded-in-source discipline) + `.claude/commands/expert-council.md` at HEAD; simulacra-shallowness caveat already on record (threads.md meta-goals) |
| d011-R11 | never disable/bypass a quality gate; report the blockage | tdd-bdd T-28; its needs-rework phrasing ("stop, leave tree untouched, report") is a T-28 v3 wording candidate |
| d011-R12 | `git add .` forbidden | CLAUDE.md `<git_workflow>` |
| d011-R13 | never stage/commit/read diary without permission | CLAUDE.md `<file_operations>` + `<git_workflow>` explicit staging |
| d011-R14 | `bookminder/__init__.py` empty; exceptions in modules | CLAUDE.md `<package_structure>` |
| d011-R15 | contributor entry format + trailer format, update on upgrade | CLAUDE.md `<project_maintenance>` (substance); trailer half is tooling-injected now (see d013-R6 reject); format detail preserved by the live `authors` list itself |
| d015-R16 | no restating comments in shell scripts | CLAUDE.md `<code_style>` — the rule is not language-scoped |
| d016-R16 | no shell comments restating next line | CLAUDE.md `<code_style>` |
| d017-R12 | naming guidance as tendency, not template | CLAUDE.md `<backlog_management>` — carries the exact phrase "descriptive and action-oriented where it makes sense" |
| d018-R6 | commit passing test + minimal impl right after GREEN | tdd-bdd T-17 (cycle-and-commits.md) — subject to the commit-grammar v3 revision per the retirement cascade, which owns this question now |
| d018-R9 | completed story moves to Completed Features section | CLAUDE.md `<tdd_discipline>` "Update TODO.md: Move completed stories..." + `<backlog_management>` |
| d018-R10 | apply instruction changes to all three files, verify cross-refs | CLAUDE.md `<project_maintenance>` final bullet (current ratified form: ask the user) |
| d020s1-R16 | delete docstrings from implemented tests | CLAUDE.md `<code_style>` Tests ("Remove docstrings from implemented tests") + tdd-bdd T-38 |
| d020s1-R23 | keep lines ≤88 as written, verify with ruff pre-commit | CLAUDE.md `<code_style>` (max line length 88, ruff via pre-commit) |
| d020s3-R20 | stage explicitly; `-A`/`.` forbidden | CLAUDE.md `<git_workflow>` |
| d020s4-R18 | undo landed change with `git revert`, never hand-reverse | tdd-bdd T-32 (cycle-and-commits.md) — d020s4-R18 is a listed source of T-32 |
| d020s5-R12 | no comments restating the assertion beside them | CLAUDE.md `<code_style>` "Do not add comments in specs files that merely restate what the code is doing" |
| d020s5-R13 | delete docstring repeating the it_ name | CLAUDE.md `<code_style>` Tests + tdd-bdd T-38 |
| d021-R13 | mandatory story status field incl. reopened | CLAUDE.md `<backlog_management>` Status Field — verbatim, written by that session |
| d021-R22 | propagate conventions to all three instruction files | CLAUDE.md `<project_maintenance>` final bullet (ask-the-user form) |

## Reroute

| rule_id | rule gist | disposition detail |
|---|---|---|
| d003-R11 | run official migration on deprecation warning before committing | reroute → tdd-bdd (cycle-and-commits): commit-history hygiene — keep history free of avoidable later cleanup commits; kin of T-20/T-33 batching family |
| d005-R4 | CI runs through same entry point as local (`pre-commit run --all-files`) | reroute → tdd-bdd (T-28 gate-integrity family): one config, one execution path — specialist concern (fires only when touching CI), not every-session constitution |
| d005-R9 | one concern per commit; split a file's changes via stash | reroute → tdd-bdd (cycle-and-commits): mechanics extend T-20/T-33; CLAUDE.md's "small, focused" already carries the principle |
| d007-R13 | if commit output lists an unintended file, stop and reset before pushing | reroute → tdd-bdd (cycle-and-commits): post-commit read-back joins T-17's read-the-staged-diff discipline; staging half already covered by `<git_workflow>` + hook |
| d009-R16 | read back commit file list and insertion count | reroute → tdd-bdd — same increment as d007-R13, same destination |
| d009-R14 | TODO/FIXME naming the open question, not a guessed fix | reroute → tdd-bdd (writing-a-spec / minimal-implementation): implement-loop comment discipline; no T covers it — v3 candidate |
| d009-R15 | never cite project docs as justification for code | reroute → tdd-bdd — pairs with d009-R14 as comment-content discipline ("It might as well say query from God") |
| d013-R10 | restore clobbered file via `git checkout --`, not from memory | reroute → tdd-bdd (T-32 family): restore-from-VCS is the same principle as revert-not-hand-reverse — v3 merge candidate into T-32 |
| d013-R11 | commit the process/rules change first, separately, then governed content | reroute → tdd-bdd (cycle-and-commits): sequencing kin of T-33 (requirements commit precedes implementation) |
| d018-R18 | bugfix and docs in separate commits; split with `git reset --soft` | reroute → tdd-bdd (cycle-and-commits): same batch-discipline family as d005-R9 |
| d020s4-R16 | prefer shorter name when context supplies the meaning | reroute → tdd-bdd (writing-a-spec/minimal): naming principle (`format(book)` over `format_book(book)`), user-verbatim — v3 candidate |
| d002-R7 | same class of mistake corrected twice → amend the process doc same turn | reroute → project-coordinator (persistence): durable-capture of corrections is the persistence protocol's job; the destination today is the skills/corpus pipeline, not same-turn CLAUDE.md edits |
| d003-R4 | "in the future we should X" → convert X to rule/config now | reroute → project-coordinator (persistence): same durable-capture family as d002-R7 |
| d004-R14 | propose lessons line-by-line for acceptance; drop valueless lines | reroute → project-coordinator (authorization): rule changes need the author's line-by-line acceptance — this rule IS the thin-CLAUDE.md ruling's ancestor and belongs with the author-approval conduct |
| d017-R16 | rule failed twice → propose executable guard, not stronger prose | reroute → project-coordinator (process evolution): the author's automation-over-prose principle (hooks = most valuable CC innovation); guides how the coordinator handles recurring failures |
| d018-R23 | guardrail hooks block only objectively-wrong actions | reroute → project-coordinator: hook/guardrail design judgment for this repo (blanket-blocking incident); pairs with d017-R16 |
| d005-R2 | partner says it's over their head → stop proposing, teach from real artifacts | reroute → pair-programming (reciprocal/mirror): dialogue conduct — how to respond to the partner's confusion; not constitution |
| d005-R16 | one Python version everywhere; surface tool conflicts, never silently lower | reroute → bookminder (repo geography): record the 3.13-everywhere policy AND the live land mine — `target-version = "py312"` at pyproject.toml:71 contradicts `requires-python = "==3.13.*"` at :11 today, 14 months on |
| d013-R13 | compress screenshots under the 500 KB hook limit, don't raise it | reroute → bookminder (repo geography): the 500 KB pre-commit limit + compress-not-relax precedent are repo facts; `sips` is a macOS-era detail |

## Reject

| rule_id | rule gist | reason |
|---|---|---|
| d019-R22 | keep commit-after-RED step in `<git_workflow>` | obsolete — commit-after-RED retired by author ruling 2026-08-14 (threads.md "COMMIT-AFTER-RED RETIRED"); the cascade reverts exactly this |
| d002-R11 | exclude diary from every pre-commit hook | tooling-solved — exclusion encoded in `.pre-commit-config.yaml` at HEAD (lines 20, 31); the config is the rule |
| d005-R13 | delete cosmetic hooks that fight agent output | one-time repo-config decision, already executed (hooks removed at HEAD); its own feasibility note warns the generic form licenses gate-weakening without author approval |
| d005-R15 | search diary with rg yourself, never delegate to a sub-agent | superseded — later user practice ratifies the opposite (threads.md working style: protect main-thread context, delegate doc-heavy reads); later-user-overrides-earlier |
| d008-R12 | slash-command bang-backtick syntax + allowed-tools patterns | era-conditioned harness mechanics — CC syntax detail, already embodied in the working `.claude/commands/*.md` files; tool-versioned knowledge, not constitution |
| d008-R13 | echo each command as plain text above its !`backtick` form | era-conditioned harness mechanics — same as d008-R12; hi.md at HEAD already implements it |
| d013-R8 | keep slash command as verbatim file, reference from rules file | era-conditioned — the current skills/commands architecture makes prompt files self-contained by construction; the GEMINI.md-collapse failure cannot recur in that form |
| d013-R6 | single Co-Authored-By trailer, acting model, second only on reported switch | tooling-solved — the harness now injects the acting model's trailer into every commit; the mid-session-switch nuance is era-conditioned manual practice |
