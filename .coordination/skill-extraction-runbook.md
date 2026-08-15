# Skill-extraction runbook

Rerunnable process for turning session transcripts into verified, author-ratified skills. Codified 2026-08-15 from the first full run (the 2025 diary corpus → tdd-bdd / pair-programming / bookminder skills). Audience: a future coordinator session with no memory of that run. Every stage below names its gate falsifiably; every claim about the first run traces to .coordination/compile/briefs.md, .coordination/threads.md, .coordination/eval-design.md, the .coordination/tools/ scripts, or the verification reports and changelogs in .coordination/compile/.

Companion records to load before executing: briefs.md (verbatim worker prompts — resend these, do not paraphrase them), eval-design.md §Compile/reduce policy (resolution rules), threads.md (live project state and standing author rulings).

## Stage-agnostic operations (apply to every stage)

- Worker routing: deliverables the author personally reads and grades → worker-fable (.claude/agents/worker-fable.md, pinned xhigh); bulk extraction/verification → Opus at xhigh; blind smoke agents → worker-opus with NO session context, skill directory only. Agent tool for single steerable tasks (transcript-resumable via SendMessage); Workflow only for fan-out/schemas/concurrency.
- Every worker self-commits its own disjoint deliverable as it reaches a consistent state: batch `git add <paths> && git commit` as one command, `git push` as a separate command, retry 4x with 2/4/8/16s backoff on network failure only, `pull --rebase` then re-push on rejection. Never `git add -A` — concurrent siblings commit disjoint files.
- Overload resilience (529 storm, first run): workers cut mid-flight are resumed via SendMessage transcript continuation with the standing instruction: resume per brief + any correction, re-check disk state before rewriting, commit incrementally. Put the incremental-commit instruction in every brief from the start.
- Watchdog: self-re-arming send_later trigger (~20 min cadence during swarms) with duties liveness-check, batch-commit of true orphans, persistence sweep (conversation-only state → committed record), per-slice resume. Drain before kill: let in-flight agents finish and self-commit before stopping a workflow (a first-run kill discarded ~357K tokens of nearly-complete work).
- Concurrency sizing: per-workflow agent concurrency is min(16, nproc-2); with nproc=4 that is 2 — slice a swarm into multiple workflows to get real parallelism.
- Formatting (all deliverables): never hard-wrap prose — one line per paragraph or bullet; tables/code exempt. No praise, no meta-narration. Claims discipline: every present-tense repo assertion carries a file:line verified against the current tree.
- Attribution discipline: never present agent synthesis as the author's position; provenance typing (user-verbatim | user-paraphrase | agent-synthesis) travels with every claim.

## 1. Pipeline as executed

### Stage 0 — SOURCE HYGIENE (dedup scan of transcripts)

Purpose: find duplicated content inside and across source transcripts before any miner reads them, so no episode is mined twice and no support count is inflated.

Tool: .coordination/tools/dupescan.py — token-shingle scan (K=100 substantive tokens, report merged runs ≥150), whitespace-normalized and glyph-stripped so two renderings of the same console output match even when the terminal re-wrapped them at different widths. That normalization is load-bearing: the first run's initial (pre-normalization) scan caught only byte-similar re-pastes (day-020 ~42% self-dup, day-007 L6396-7658 = L1852-3114) and missed that day-020 was ONE conversation rendered FIVE times in 3 rendering families (session banners L3/L7207/L21811/L31130/L45521) — miners then mined the same turns up to five times.

Disposition per finding: shard the file on session banners with original-line-number prefixes (so locs need no arithmetic), give miners skip-ranges, or repair the source (day-020/day-007 were repaired delete-only, with per-ref positional byte-equality gates against pre-repair blobs and remap tables at .coordination/tools/day-020-remap.md and day-007-remap.md).

Gate (falsifiable): dupescan output reports zero duplicated regions ≥150 tokens across the corpus, OR every reported region has a written disposition (shard/skip/repair) before any miner launches.

Artifacts: dupescan.py; remap tables in .coordination/tools/; repair plans/reports (.coordination/day-020-repair-plan.md, day-020-repair-report.md).

### Stage 1 — MINE (sharded swarm, schema v2.2, validator gate)

Purpose: extract the author's philosophy, skill rules, failure modes, pairing conduct, and council episodes from transcripts into structured YAML with provenance typing.

Tool: .coordination/tools/mining-slice-v2.2.js (arg-sliced Workflow; Opus miners at xhigh, one per file/shard). Schema v2.2 sections: philosophy (statement + source typing + mandatory quote for user-verbatim + loc + feeds), skill_rules (rule_id, rule, because, because_source, evidence, taught_or_enforced, skill_target, overlap, feasibility), failure_modes (controlled vocabulary + era_class + detector_family + quote + loc + user_intervention + outcome + detector_candidate + rule_origin), pairing_rules (mirror | reciprocal | council-mechanics), council_episodes (per-persona fidelity: faithful | caricature | fabrication), pairing_gems, gaps (absence made distinguishable from oversight), parked. Each miner brief carries per-file notes: era, user-marker format ("> " col 0 vs Gemini box "│  > " two spaces), known incidents, duplication warnings, shard line-prefix convention.

Gate (falsifiable): .coordination/tools/validate_mining.py exits 0 on every YAML — required fields, enums, loc format, quote-verbatim-against-source (whitespace/glyph-normalized). First run gated post-hoc and needed a repair pass (e89c304, 24/24 OK); the author's standing directive is that future swarms embed the validator in miner instructions — run it per file BEFORE self-commit.

Artifacts: .coordination/mining/v2/*.yaml (24 files first run), .coordination/mining/pairing/*.yaml (council-fidelity trial); v1 pilots kept in mining/v1/ (superseded, do not read at compile).

### Stage 2 — CONTRADICTION LEDGER (evidence-ranked resolution, author ratifies judgment-calls)

Purpose: resolve corpus-internal and corpus-vs-repo contradictions BEFORE compile, so compile workers execute rulings instead of improvising.

Tool: worker-fable with briefs.md §1 verbatim. Resolution rules (eval-design.md, author-approved): (1) user-verbatim > user-paraphrase > agent-synthesis; (2) among user statements, later date overrides earlier; (3) agent-era artifacts never override an earlier user ruling; (4) propose, never resolve silently — every entry ships both sides verbatim. Judgment-calls listed first; the author ratifies interactively and the ratification record is appended to the ledger.

Known brief defect + fix (briefs.md): instruct that threads.md/eval-design.md session rulings are SETTLED ADJUDICATIONS — usable to resolve corpus contradictions, never eligible as a contradiction side (the first run's L-03/L-04 were self-litigation between coordinator notes, withdrawn).

Gate (falsifiable): no ledger entry with confidence=judgment-call lacks an author ruling in the ratification record; every rule-mechanical entry names which rank decided it.

Artifacts: .coordination/compile/contradiction-ledger.md (first-run ratification: b8b1292).

### Stage 3 — COMPILE (per-skill workers, optimized build + sidecars, four verification gates)

Purpose: compile the corpus into portable skills — optimized build (no provenance/dates/day-refs in skill text) with debug-build traceability carried by sidecars.

Tool: one worker-fable per skill, briefs.md §§2-4 verbatim, with the mid-flight correction (briefs.md §5) folded into FORM from the start: .claude/skills/skill-creator/ is the authoring authority (progressive disclosure, description = what+when, quick_validate), project-coordinator/ is only a shape example. Every rule: crisp imperative + WHY, an ID (T-NN/P-NN/B-NN), and "rationale unrecovered" where the corpus does not carry the WHY. Sidecars per skill: rule-index (ID → source → provenance type → detector/rubric/UNFALSIFIABLE flag) and disposition (EVERY corpus id: compiled→ID | merged-duplicate→ID | rejected(reason) | reroute:<owner> — nothing silently dropped).

Gates (all four, falsifiable):
1. quick_validate.py exits "Skill is valid!" per skill directory (independent coordinator re-run, not worker claim).
2. Disposition completeness: script extracts every rule_id/gem_id/id from the mining corpus and asserts each appears in some disposition file (first run: 804/804 after the 95 orphaned skill_target:claude-md ids were captured in pending-claude-md.md).
3. Falsifiability audit: every rule-index row carries detector-covered | rubric-item | UNFALSIFIABLE; the UNFALSIFIABLE list is presented to the author (first run: 1, T-06).
4. Blind smoke tests: worker-opus agents with no session context act on scenario briefs (briefs.md §6) reading only the skill directory; session-context coordinator judges each response against rule IDs. First run 6/6 substantive pass; the smoke agents also surfaced a live repo divergence (is_cloud vs --filter cloud) — treat smoke output as a fresh-eyes audit channel, and expect return-length-cap violations (conduct gap, not skill gap).

Artifacts: .claude/skills/<skill>/ + .coordination/compile/rule-index-*.md + disposition-*.md + pending-claude-md.md.

### Stage 4 — TRANSCRIPT RE-VERIFICATION (per-source verdicts against transcript windows)

Purpose: verify what the validator never checked — miner SUMMARY vs TRANSCRIPT. This stage was discovered mid-review by the author: quote-verbatim checking says nothing about episode fidelity, generalization overreach, or context the miner missed.

Tool: Opus verifier slices (8 in the first run, after a pilot on P-12/P-14's 17 sources). Method per compiled-rule source row: pull the transcript window around the evidence loc (~100 lines before, ~60 after; .coordination/tools/rule.py -c automates window extraction — query structured YAMLs with the parser, never grep, per author directive) and judge four axes: quote exactness, episode fidelity, generalization fit, missed context. Verdicts: FAITHFUL | DISTORTED(subtype: embellished-because, misattribution, dropped-qualifier) | OVERREACH | UNDERREACH, plus duplicate-episode annotation `(=X)` when multiple corpus entries are one author turn.

Gate (falsifiable): every source row of every compiled rule has a verdict row citing the window it was judged in; bad-loc count is zero or each bad loc is repaired; systemic findings (duplication families, relay mislabels, index mis-filings) are extracted into the Stage 5 judge briefs, not left buried in tables. First-run aggregate: ~740 rows, ~86% FAITHFUL, zero bad locs.

Artifacts: .coordination/compile/provenance-verification-*.md.

### Stage 5 — JUDGE v2 (same-tier judges adjudicate and apply; changelog as review surface)

Purpose: convert verification findings into applied skill edits without per-item author round-trips (author-authorized mode: "get an improved v2 then continue manual review").

Tool: one worker-fable judge per skill, consuming that skill's verification reports plus pilot roll-ups and systemic-correction notes. The judge DECIDES and APPLIES rewrites/splits/new-rules directly to the skill, updates rule-index and disposition coherently (duplicate annotations, dropped sources recorded at their rows, relabels), re-runs quick_validate, and writes skill-v2-changelog-<skill>.md where EVERY change carries its reason + verification citation. Judges rewrite rules from the VERIFIED EPISODE, not the corpus entry, when the entry is distorted (first-run P-40 was compiled from a DISTORTED entry's corrected episode). No protective freeze on author-approved v1 pages — but the changelog marks which pages were v1-approved, because the v1→v2 diff on an approved page is the method's own quality gauge.

Gate (falsifiable): validators green post-merge on all skills; no changelog entry lacks a verification citation; no rule is left with zero faithful sources (remove the rule or find real evidence — first run removed none, dropped 3 dangling/misattributed sources, all recorded).

Artifacts: skills at v2 + .coordination/compile/skill-v2-changelog-*.md.

### Stage 6 — AUTHOR REVIEW (digest first, pages as ratification objects, sequential presumption)

Purpose: convert committed skills into ratified rules. Committed ≠ ratified — nothing is repo rule until the author approves.

Method (all author-ruled): one skill at a time, smallest first. Present a Was/Now/Why DIGEST first (pairing-v2-digest.md is the ratified template — raw diffs are unreadable on mobile), then the full pages, which are the ratification objects. Sequential-presumption rule: within a sequential review, feedback on item N may be presumed to imply approval of items 1..N-1 — but CONFIRM the presumption explicitly; it never applies to out-of-order replies. Review technique that works: the author dry-run-tests a rule's interpretation blind, then rule-index → mining YAML → transcript window looks up the inciting incident (this surfaced a real compile defect, P-12's dropped census trigger). Ephemeral review aids retire after consumption (digests git-rm'd post-ratification); verification reports stay (evidence cited by rule-indexes); diffs are never committed.

Gate (falsifiable): explicit per-file author approval recorded in threads.md; any presumed approval carries the author's confirmation of the presumption. First run: pair-programming fully ratified 2026-08-15.

## 2. Phase-1 improvements (fix mining so verification has less rework)

Each item below is verified against the first run's record. Items (a)-(i) are ordered by pipeline position, not weight — (d) is the big architectural change.

(a) Run the wrap-normalized dupescan BEFORE mining and dedup at source. The first run scanned first but with a weaker scanner; day-020's five renderings survived into the shards, inflated source counts corpus-wide (apparent rule support inflated ~20%, changelog §4), and cost a mid-pipeline source-repair detour. Sharding makes this worse, not better: sharding blinds miners to repeats, so any sharded run REQUIRES a cross-shard dedup stage (lesson on record, threads.md).

(b) Verify quotes character-exact in EVERY field at mining time, not just quote:. validate_mining.py audits only quote: fields; a fabricated user-quote in day-018's user_intervention field slipped the gate and was caught only by a later repair agent. Extend the validator to scan every string field for quoted-looking spans and verify them against source; run it inside the miner loop (per the standing directive), not post-hoc.

(c) Because-clauses only from evidence; "rationale unrecovered" is mandatory otherwise — AT MINING TIME. Embellished-because was the top distortion class in re-verification (33 rows, narrowly ahead of misattribution's 30): miners invented six-checkmark summaries, "whole working tree" losses, and enumeration claims the windows do not contain, and stamped agent-synthesized because texts because_source: user-verbatim. The compile briefs already mandated "rationale unrecovered"; move the mandate upstream into the miner schema and have the stage-1 verify pass (d) check the because against the window.

(d) THE ARCHITECTURAL CHANGE: pull transcript-window verification INTO the mining pass. Stage 4 existed only because nothing ever checked miner summary against transcript — it was discovered mid-review and re-adjudicated ~740 rows months of context later. Next run: pipeline a verify-stage per mined unit immediately after extraction — miner emits YAML, a verifier agent immediately re-reads each unit's window (rule.py -c method, four axes, verdict row) before the unit is banked. Build it as a Workflow in the detector-suite pattern (.coordination/tools/detector-suite-build-v1.js): per-unit agents, a structured result schema that demands actually-run verification results ("not intentions"), and an aggregation step auditing coverage. Compile then consumes only FAITHFUL-or-corrected units, and stage 4 shrinks to a spot-check.

(e) Enforce provenance typing mechanically, including relay detection. Gemini-relay text (author pasting another model's output) was mislabeled user-verbatim (d019-R14/16/17 + the day-010 relay cluster; 8 relabels in the bookminder judge pass alone), and an agent-authored CLAUDE.md definition was quoted as the author's words (p010-R18). A user-verbatim label must be checked against WHOSE text occupies the cited line: text inside compaction summaries, quoted model output, or agent-written files is not the author's voice regardless of the user-marker prefix.

(f) Complete the skill_target vocabulary BEFORE launching, and give every target a compile owner. The pair-programming target entered the schema only at the v2.2 relaunch (the pilot and first v2 launch ran on the two-skill split), so compile had to sweep conduct-shaped rules regardless of tag and reroute; the claude-md target had no compile consumer at all — 95 ids surfaced as a coverage-check gap and needed pending-claude-md.md written after the fact. At schema design: enumerate targets, name each target's downstream consumer, and freeze before the swarm launches.

(g) Merge policy for compile: two sources are the same rule only if they name the same OBSERVABLE VIOLATION. Over-merging swallowed distinct moves: P-14's 13 independent episodes hid three standalone rules (restate-the-reasoning → P-40, receive-partner's-self-criticism → P-41, write-don't-propose — recovered only by the pilot's over-merge audit), and P-12 carried a merged source (p004-R11) with zero expression in the compiled text. Put the test in the compile briefs verbatim, and require the disposition entry for every merged-duplicate to name which clause of the target rule expresses it.

(h) Structured-query tooling (rule.py) and stable ids from day one. rule.py was built mid-run and hardened 3x (quoted ids, abbreviated-token warnings, bare-LNNNN windows); id defects cost verification time: dual-id collisions across corpus dirs (p021-R2, p021-R8 each exist in v2/ and pairing/ meaning different rules), ad-hoc alias suffixes (p021t-R2), a dangling id ("v2 p019-R29"), and a mis-keyed gem. Next run: id scheme includes the corpus dir, validator rejects cross-file collisions, rule.py (extended for the new corpus format) ships before the first miner launches.

(i) Summary-quotation awareness: compaction summaries silently normalize spelling, so quote-hunting must be normalization-aware. p020s5-R10 carried user-verbatim on an agent compaction restatement whose spelling was silently cleaned ("possitions"→"positions", "carricature"→"caricature") — a character-exact match against a summary line can be a false provenance proof. Rule: a quote whose window is a compaction summary or model re-quote is second-hand (see P-09); preserved typos are positive evidence of a primary author turn.

(j) NEW (found in record): give mined units a turn-identity key. Beyond source-level duplication, one author turn became multiple corpus entries across sections and files (p006-R3/d006-R15 = one turn; the "PathResolver my ass!" turn = five entries across two rules). The `(=X)` same-turn annotation had to be retrofitted at v2. Key each mined unit on the author-turn loc so same-turn dedup is mechanical at compile.

(k) NEW (found in record): define the loc/citation convention for the NEW corpus format before schema freeze. Every first-run tool assumes rendered day-NNN.md line numbers (validate_mining.py LOC_RE, rule.py window extraction, dupescan globs day-*.md). The incoming corpus is native JSONL: decide the citation scheme (file + line or event index), extend all three tools, and validate on a sample BEFORE writing the miner schema — otherwise the entire verification substrate (transcript windows) breaks silently.

(l) NEW (found in record): brief-quality items to fold in at source: ledger brief fix (threads.md rulings are settled adjudications, never contradiction sides — briefs.md §1 defect note); skill-creator-as-authoring-authority in FORM from the start (briefs.md §5 note); expect and pre-empt the return-length-cap conduct gap in smoke briefs; refresh the L-NN enumerations in compile briefs' AUTHORITY ORDER mechanically after a ledger refresh (they are snapshots).

## 3. Intake protocol for the incoming 2025 corpus

Two sources, two paths (the local-machine delivery brief at the top of threads.md instructs the author's local session; this section is the cloud coordinator's half):

1. Local 2025 JSONL backups → claude-dev-log-diary/jsonl/local-2025/. Committed by the author's local session; no scrub gate on record for these.
2. GitHub-infrastructure session transcripts (currently uncommitted on the author's machine; from PR runs on GitHub infra — the xs-tool's inciting incident) → claude-dev-log-diary/jsonl/github-2025/ ONLY AFTER the secret-scrub gate: `python3 .coordination/tools/scrub_scan.py <folder>` (exit 1 on any credential-shaped finding), every finding reviewed with the author — mask or drop, never rewrite silently, never commit with findings unresolved.

Then, in order:

3. Dupescan vs existing corpus (Stage 0): extend dupescan.py to the jsonl/ dirs (its file glob and diary path are hardcoded to day-*.md) and make normalization operate on extracted message text, not raw JSON (JSON escaping would defeat token matching). Scan new-vs-new AND new-vs-existing — the 2025 day-files are rendered console captures of sessions the JSONL may contain natively, so cross-corpus duplication is EXPECTED, not anomalous; the disposition question is which rendering is authoritative per session, decided with the author before mining.
4. Schema design for the new pass, with two flags raised to the author BEFORE launch: (i) the diverged-era caveat — later 2025 material diverges from BookMinder into xs-tool development (author-stated at commissioning); still minable for pairing/conduct lessons, but the skill_target vocabulary likely needs an xs/tooling bucket with a named compile owner (improvement f); (ii) the JSONL loc convention (improvement k). Expected new evidence: the commit-after-RED era the day-file corpus never covered — note the author has since RETIRED commit-after-RED (threads.md ruling 2026-08-14), so mined evidence for it feeds history/eval design, not skill rules.
5. Improved mining pass: Stage 1 with improvements (a)-(l) applied — mine→verify pipelined per unit (d), validator embedded and extended (b), because-discipline (c), relay detection (e), turn-identity keys (j).
6. Downstream rerun per briefs.md: refresh the contradiction ledger first (its brief takes the new YAMLs; apply the §1 defect fix), author ratifies new judgment-calls, then re-send the three compile briefs unchanged (they read corpus and ledger from paths) with mechanically refreshed L-NN enumerations; then stages 4-6 (stage 4 reduced to spot-check if (d) held).

## 4. Open questions carried forward

- Because-clause form (threads.md 2026-08-15): the trailing "Because X" form is a hypothesis to A/B at BENCHMARK stage — C2 condition run with skill variants (because-trailing / stripped / inline-terse), measuring rule-following delta vs token cost. Not a pre-ratification test. Candidate skill-authoring principle once measured.
- Whether this runbook should itself become a portable skill: author's position at commissioning — maybe too meta; revisit after one rerun proves the codification.
