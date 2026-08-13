# Pending: claude-md-targeted rules (gardening-pass input)

These corpus entries carry skill_target: claude-md — repo-constitution rules with no compile owner by design; the three-skill extraction deliberately excludes CLAUDE.md changes. The gardening pass dispositions each one: amend CLAUDE.md | already-covered | reroute to a skill (single-ownership per ledger L-07) | reject. Until then this file closes the disposition coverage gap (verified: with it, all 804 corpus ids are accounted for).

| rule_id | rule (first line) |
|---|---|
| d002-R7 | When the user corrects the same class of mistake twice, stop patching the instance and amend CLAUDE.md in the same turn so the correction does not need repeatin |
| d002-R8 | Keep the project's rules in the single canonical CLAUDE.md; never create a parallel principles or conventions document. |
| d002-R9 | When merging one rules document into another, verify item-by-item that nothing was dropped, and show the comparison rather than asserting completeness. |
| d002-R11 | Exclude `claude-dev-log-diary/` from every pre-commit hook rather than skipping hooks per-commit. |
| d002-R17 | Keep `__init__.py` files empty; if a linter demands docstrings in them, configure the linter rather than editing the files. |
| d002-R19 | A commit message must describe the change the commit actually makes; amend it when it does not. |
| d003-R2 | Run the formatters/hooks before committing, then re-stage the files the hooks modified, |
| d003-R4 | When you catch yourself writing "in the future we should X", stop and convert X into |
| d003-R6 | Never stage with `git add .` or `git add -A`; name every path explicitly. |
| d003-R7 | Relocate a file with a move, never a copy; if a copy is unavoidable, delete the source |
| d003-R8 | Keep config files and source free of explanatory comments; if the explanation is worth |
| d003-R11 | When a tool emits a deprecation warning during a commit attempt, run its official migration |
| d003-R14 | Record the acting model version in pyproject.toml contributors and refresh it whenever the |
| d004-R10 | Move tracked files with `git mv`; never emulate a move by reading a file and writing a new one, and never plain-`mv` then `git rm`. |
| d004-R12 | Keep documentation in docs/ with lowercase, underscore-separated filenames; do not drop SHOUTING_FILES into the project root. |
| d004-R13 | Do not add a comment that restates the command or line beneath it. |
| d004-R14 | When adding lessons to CLAUDE.md, propose them for line-by-line acceptance and delete any line the user judges valueless. |
| d004-R20 | Stage files explicitly by name; never `git add .`. |
| d005-R2 | When the user says a proposal is over their head, stop proposing and explain how the existing setup actually works, reading the real artifacts (.git/hooks/pre-c |
| d005-R3 | Never use `git commit --no-verify`; if a hook blocks the commit, fix the hook configuration and then use the hook itself to prove the fix works. |
| d005-R4 | Run CI through the same entry point as local development (`pre-commit run --all-files`), never by invoking ruff/mypy directly, so both read one set of excludes. |
| d005-R9 | Commit in logical batches of one concern each, splitting a single file's changes across commits when they serve different concerns (stash the rest, commit the s |
| d005-R10 | Write the commit message against the diff the reader will actually see; drop references to work-in-progress states that were corrected before staging and theref |
| d005-R11 | Never run `git add .` or `git add -A` in this repo; stage files explicitly by name. |
| d005-R12 | Do not require type annotations in spec files — exclude `specs/` from mypy while keeping ruff lint and format on them. |
| d005-R13 | When a purely cosmetic hook repeatedly fights the agent's natural output, delete the hook rather than build machinery to auto-stage its fixes. |
| d005-R15 | Search the diary transcripts with `rg` directly rather than delegating to a sub-agent, and report the match counts and patterns used. |
| d005-R16 | Keep the single Python version declaration consistent across pyproject.toml, CLAUDE.md and docs/; if a tool cannot target it, surface the conflict instead of si |
| d005-R17 | Record deferred work as an explicit pinned entry at the top of TODO.md at the moment of deferral, and never delete, demote or renumber an existing pinned entry  |
| d005-R18 | Order the backlog by dependency (root-cause fix first, then the work it unblocks) and fix the ordering before committing the list, not after. |
| d006-R10 | Append to the pyproject.toml contributors list when the model changes; never replace an existing entry. |
| d006-R11 | Do not bump the package version as a side effect of a maintenance sweep; a version change is a separate decision requiring its own reason. |
| d007-R12 | Keep docstrings to a single line on public functions, drop them entirely on private ones, and never emit NumPy-style Args/Returns blocks with underlines. |
| d007-R13 | Never stage with `git add -A` or `git add .`; name every path, and if the commit output lists a file you did not intend, stop and reset before pushing. |
| d007-R14 | A commit message may claim only what the diff does; never attribute a benefit (portability, dependency removal, platform independence) the change does not actua |
| d007-R20 | When a linter deletes a line, delete the comment that existed to explain it — and never replace a stale comment with a fresh one that restates the code. |
| d008-R3 | When asked to record why a rule exists, ask the human for the actual cause; never supply a plausible-sounding rationale of your own invention. |
| d008-R4 | Add a new rule to the existing section whose concern already owns it; create a new top-level section only when no existing concern covers it. |
| d008-R5 | When a plan removes a section, enumerate every line it contained and name where each one lands; a deletion may never ride along on a consolidation that has not  |
| d008-R12 | In a `.claude/commands/*.md` slash command, wrap every shell command in backticks after the bang — !`tree -h .` — and declare `allowed-tools` with per-command p |
| d008-R13 | In a slash command, print each command as plain text immediately above its executed !`backtick` form. |
| d008-R15 | Never cite a project rule you have not located; quote the section, or say plainly that no rule covers the case. |
| d009-R14 | When a design question has no answer yet, leave a TODO/FIXME naming the open question rather than a comment restating the code or a guessed fix. |
| d009-R15 | Never cite the project's own documentation as the justification for a line of code; explain what the code does or delete the comment. |
| d009-R16 | Never stage with `git add -A` or `git add .`; name every path, and read back the commit's file list and insertion count before moving on. |
| d009-R17 | A commit message may claim only what the diff does; if it names a capability ("handles errors gracefully"), point at the code that delivers it or drop the phras |
| d009-R18 | Write project documents in plain markdown with word markers such as [COMPLETED]; no emoji status decoration in TODO.md, docs/ or commit bodies. |
| d009-R19 | Put no comments inside bash code blocks in documentation; the block must be copy-pasteable verbatim, with all explanation in the surrounding prose. |
| d010-R13 | Stage files explicitly by name; never `git add .` or `git add -A`. |
| d010-R14 | Relocate tracked files with `git mv`; when `git mv` reports "destination exists", |
| d010-R15 | Mirror any rule or slash-command added to CLAUDE.md into AGENTS.md (and GEMINI.md) in |
| d010-R16 | /expert-council convenes Kent Beck, Dave Farley, Dan North and Freeman & Pryce for |
| d011-R11 | Never disable, comment out, or bypass a quality gate (`--no-verify`, editing |
| d011-R12 | Stage files explicitly by name; `git add .` is forbidden in this repo. |
| d011-R13 | Never stage, commit, or read files under `claude-dev-log-diary/` without explicit |
| d011-R14 | Keep `bookminder/__init__.py` empty; put a new domain exception in a module, not |
| d011-R15 | Record an AI contributor in `pyproject.toml` as `{name = "<Full Model Name> |
| d013-R5 | Treat permission to read `claude-dev-log-diary/` as scoped to the exact file (and line range) named in the grant, and re-ask for anything outside it. |
| d013-R6 | Sign commits with a single `Co-Authored-By:` trailer naming the model actually doing the work, and add a second trailer only when the user reports a mid-session |
| d013-R8 | Keep a custom slash command as a verbatim file under `.claude/commands/<name>.md` and reference it from the rules file; never collapse it into a summary or a me |
| d013-R9 | Amend a rules/constitution file with a targeted edit against the exact current text; never call a whole-file write to add a section. |
| d013-R10 | Restore a clobbered tracked file from version control (`git checkout -- <file>`), not by rewriting it from your own context. |
| d013-R11 | Commit the process/rules change first and separately, then the content change it governs. |
| d013-R12 | Write the commit message strictly against the staged diff; delete any sentence describing files you did not stage. |
| d013-R13 | Keep committed screenshots under the 500 KB pre-commit limit by converting PNG to JPEG (`sips -s format jpeg -s formatOptions 70`) rather than raising the limit |
| d014-R9 | Access to claude-dev-log-diary/ is granted per-request and per-range: read |
| d015-R14 | Treat permission to read claude-dev-log-diary/ as scoped to the single file named in the grant, and only for the stated purpose of recovering interrupted contex |
| d015-R16 | Do not write comments that restate the line beneath them, in shell scripts as much as in Python. |
| d016-R11 | Write commit bodies that state the benefit, with no "This commit ..." preamble, no filename |
| d016-R16 | Do not add comments to shell scripts that restate the command on the next line. |
| d017-R12 | Write naming guidance as a tendency, not a template — "descriptive and action-oriented |
| d017-R16 | When a process rule has failed twice, propose an executable guard (a Claude Code |
| d018-R6 | Commit the passing test plus minimal implementation immediately after GREEN, before starting any refactoring. |
| d018-R9 | Move a completed story into TODO.md's "Completed Features" section and remove it from the backlog list; do not edit the backlog line in place. |
| d018-R10 | When amending the instruction files, apply the change to CLAUDE.md, AGENTS.md and GEMINI.md, and verify the cross-reference note in each names all three. |
| d018-R18 | Keep a bugfix and its documentation in separate commits, splitting them with `git reset --soft` if they were staged together. |
| d018-R19 | Remove tracked files with `git rm`, not `rm`. |
| d018-R23 | In a guardrail hook, block only actions that are objectively wrong in this project; leave context-dependent tool choices to the agent's reasoning. |
| d019-R22 | Keep the commit-after-RED step in `<git_workflow>`, not only the RED-verification step in `<tdd_discipline>`. |
| d019-R23 | Keep the `git add .` prohibition mechanized as a PreToolUse hook rather than as prose alone. |
| d020s1-R16 | Delete docstrings from implemented tests; the `it_` name and the assertions are the specification. |
| d020s1-R22 | Stage files explicitly by name; never `git add -A` or `git add .` (a PreToolUse hook blocks it). |
| d020s1-R23 | Keep lines within 88 characters as you write them and verify with ruff before committing, rather than discovering the violation in a failing pre-commit hook. |
| d020s1-R24 | Never load a `claude-dev-log-diary/day-0NN.md` in full; search it with ripgrep, or read the paired gemini-summary first and locate the day split before reading. |
| d020s3-R18 | Never access claude-dev-log-diary/ without explicit permission, and when permission is granted, restate the constraints before the first command. |
| d020s3-R20 | Stage files explicitly by name; `git add -A` / `git add .` are forbidden. |
| d020s4-R16 | Prefer the shorter name once the surrounding context (type hint at the definition, argument name at the call site) already supplies the meaning. |
| d020s4-R18 | Undo a landed change with `git revert <sha>` after checking the working tree is clean, never by hand-reversing the diff. |
| d020s5-R10 | Stage files explicitly by name; never `git add .` and never `git add -u`. |
| d020s5-R12 | Do not add comments that restate the assertion beside them (`# No crash`, |
| d020s5-R13 | Delete a docstring that repeats the it_ name; the code is the specification. |
| d021-R13 | Every story card carries a mandatory `status` of backlog | in_progress | done | reopened | |
| d021-R22 | When a convention exists in one agent-instruction file, propagate it to CLAUDE.md, AGENTS.md |
| d021-R23 | Before adding a section to CLAUDE.md, search for the section that already covers the topic |
| d021-R24 | Stage files explicitly by name; `git add -A` and `git add .` are blocked and must not be |
