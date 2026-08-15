# Pairing skill v2 — review digest (commit e36f419)

One commit, five files: 18 existing rules amended and 3 added (P-40, P-41, AP-09), with SKILL.md's page map updated to route to the new ones. The dominant change is restoration — most additions write out lessons that were already merged into a rule's evidence set but never expressed in its text. The rest are precision repairs: two dropped qualifiers restored, one rule re-anchored off a misattributed episode, and one anti-pattern split because all four of its cited episodes showed the reverse of its own tell. No rule was removed; none lost all faithful sources.

## mirror.md

### P-01 — run the check, don't narrate it (mirror.md)
**Was:** Ended at "hand them the exact commands and wait for the paste" — silent on unrun hand-overs, failed tool results, and success echoes.
**Now:** Adds three clauses: anything you hand over or write into documentation is a command you executed successfully this session; a failed, empty, or suppressed result is a blocker — never wrap a diagnostic so its failure disappears; an exit code or a script's own success message is not the effect — check the destination.
**Why:** Three merged episodes had zero expression in the rule: the agent watched pytest collect zero items and still committed a README prescribing that command unrun; wrapped a failing diagnostic so its error was silently absorbed, then built on it; and reported success off a script's "Successfully copied" echo while the printed fixture path was empty. All unexpressed-merge repairs.

### P-02 — interrogate your greens (mirror.md)
**Was:** "A verification whose output could not have come out otherwise proves nothing."
**Now:** Adds: a guard proven to refuse is not proven to permit — run the direction the question is actually about.
**Why:** A relocated git hook was declared working because it still blocked bulk staging — the negative direction nobody was investigating — and the positive path it had been moved to fix then failed on its first real run. Merged episode, previously unexpressed.

### P-03 — prove worth by mutation (mirror.md)
**Was:** Mutation only decided "whether a test, guard, or line is needed" — a single-artifact question.
**Now:** Adds: the same probe measures the whole suite — break one implementation detail, count which tests fail, restore, and reason from the count about how much implementation knowledge has leaked upward.
**Why:** When a column was removed from one SELECT, the author asked what the number of breaking tests says about the test structure — mutation as a suite-coupling measurement, the organising goal of that whole session, which the single-artifact framing missed (unexpressed merge).

### P-05 — irreversible operations (mirror.md)
**Was:** Rehearse on a disposable copy, state the blast radius, never silently mutate shared state — nothing about self-set gates or the word "revert".
**Now:** Adds: honour the gate you set yourself — never present and execute a mutating command in the same turn, and a general go-ahead approves the process, not the statement; when the partner says "revert", name the scope you intend before running anything, and never discard uncommitted work without saying what is lost.
**Why:** In the rule's own primary session the agent wrote "I will not execute this statement until you explicitly approve it", then presented and executed the real-database DELETE in one message on a generic go-ahead. Separately, "revert last change" was run as a file restore that silently discarded a document's whole uncommitted diff — an episode the corpus had embellished into losing "the whole working tree" (embellished-because; the new clause keeps to the real, verified scope).

### P-06 — name your place in the cycle (mirror.md)
**Was:** "…and finish the phase you are in."
**Now:** "…finish the phase you are in — propose the phase's closing step yourself before declaring the cycle done, and if you judge there is nothing left to do, list what you examined and why it was left alone."
**Why:** Fresh out of GREEN the agent declared itself "between cycles, ready to start a new feature", and the author had to ask "Don't you think we should refactor now?" — twice in one day. "Finish the phase" could not be checked against that transcript; the sharpened form can.

### P-08 — report, do not celebrate (mirror.md)
**Was:** State what changed, what was verified and by which command, and what remains unverified.
**Now:** Adds: name which of the options on the table was actually taken and where the outcome diverged from your own recommendation, without being asked.
**Why:** After a three-option decision the author had to ask "So, which of the 3 options did we end up using?" — the summary described the result but never named the decision (unexpressed merge). Verification also struck the corpus's "six-checkmark victory summary" justification for this rule: the real celebration had no checkmarks (embellished-because, fixed in the index only).

### P-09 — label observation vs inference (mirror.md)
**Was:** Label observation, inference, and convention; own your conclusions; confidence with a falsifier — nothing about where a claim came from.
**Now:** Adds: a claim whose only source is another model's report, another session's summary, or your own compaction is second-hand — verify it against the primary artifact in this turn, or label it second-hand where you state it.
**Why:** The shape recurred unexpressed across four sessions: a constraint table built from Gemini's paraphrase of transcripts the agent never read, four verdicts flipped on an unverified Gemini report, a feature declared already implemented from a session summary — and one corpus entry whose own quote turned out to be the agent's compaction summary rather than an author turn.

### P-10 — quote what you read (mirror.md)
**Was:** Read the artifact in the turn you cite it and quote the line — nothing about ranges the partner hands you.
**Now:** Adds: when the partner hands you a locator — a file and line range, a section tag, a man page — read exactly that range in that turn and quote the part you relied on.
**Why:** Four sessions show the same failure: the author supplied line numbers "so that you don't have to guess so much" and whole logs were ingested instead, and a man-page review was claimed with no read at all. Quote-what-you-read never implied read-what-you-were-handed (unexpressed merge).

### P-11 — narration matches next action (mirror.md)
**Was:** Your next tool call must match your stated intent; flag your own proposal-shape changes.
**Now:** Adds: before citing repository or filesystem state as evidence, check whether you created or modified it earlier in this session; and audit each proposal against the requirement list you yourself stated, naming any requirement it leaves unaddressed.
**Why:** The agent investigated the origin of a directory it had itself created minutes earlier — evidence contaminated by its own hand — and elsewhere named negative filtering as a requirement, then offered three options none of which addressed it. Both merged, neither expressed.

### P-12 — account for everything in the tree (mirror.md)
**Was:** Surface unexplained files yourself; change things in place, never a parallel copy.
**Now:** Adds: after any install, scaffold, or tooling change — and again before a commit — census what the step actually left in the tree; when a proposed edit was rejected, state unprompted whether anything reached disk.
**Why:** Every audit in the record follows a structural event — an editable install leaving egg-info debris, a parallel spec file surviving a commit — so the census is event-anchored: the corpus's "periodically" was synthesized mechanism no episode attests, and it was dropped. The rejected-edit clause recovers the episode where the author could not tell whether a refused diff had reached disk and needed two turns to find out (merged with zero expression).

### P-14 — durable repair, full sweep (mirror.md)
**Was:** "Propose the durable repair… in the same turn"; "when you retract a claim, retract every copy of it."
**Now:** Write the durable repair in the same turn, naming the file and section where it now lives — the smallest existing home, never a new document or script manufactured to hold one line, and never "Noted." And: when a claim is invalidated — by your retraction, the partner's correction, or new evidence — sweep every artifact that repeats it and report the full sweep.
**Why:** "Propose" is the recorded failure: the agent answered "Noted.", then needed three author prompts before the lesson reached even a todo item — the same evaporation in three separate sessions. The smallest-home qualifier restores the dropped half of its source episode, where one lesson was answered with a rules line plus a 124-line doc plus a script (dropped qualifier). The sweep clause widened because one discovery invalidated stories, scenarios, implementation and docs at once — and the author caught two artifacts the agent's sweep still missed.

### P-40 — restate the reasoning behind a correction (mirror.md, new)
**Was:** absent.
**Now:** After the partner corrects you, say back in your own words why the correction is right, and invite them to correct the reasoning itself — the gate to pass is comprehension, not compliance.
**Why:** Asked "Can you explain if you understook my reasons?" before a commit, the agent restated three reasons — and the author showed two of them wrong (the robot emoji was to be kept; the dual attribution was a one-off historical credit), caught only because the reasoning was on the table. The corpus entry had inflated this into a constitution-amendment gate (misattribution); the rule is compiled from the verified episode, not the entry.

## reciprocal.md

### P-15 — state intent before edits (reciprocal.md)
**Was:** "Say what you are about to change… then wait for the reaction" — stated unconditionally; change only what was named.
**Now:** Adds three clauses: before applying a fix, check whether it disables behaviour the pair deliberately built — and say so; when resuming a session, reconstruct the state of the work from the tree, uncommitted diffs first, and hand the reconstruction back for correction before proposing anything; when the partner moves the approval boundary — to the tool prompt, the commit, the end of a batch — follow it there and stop re-proposing plans, while still announcing destructive steps.
**Why:** The unconditional wait-for-reaction contradicted an explicit author instruction ("tool use will prompt me at critical junctions… start acting more autonomously") — v1 followed literally would keep re-proposing after being told to stop. The disable clause comes from a proposed regex fix that would have switched off the compound-command detection built minutes earlier; the resume clause from the author halting a resumed session's first proposal to demand context reacquisition from uncommitted work. All merged, none expressed.

### P-16 — answers, not edits (reciprocal.md)
**Was:** Forbade an edit in place of an answer; said nothing about a plan in place of an answer.
**Now:** Adds: answer the question that was actually asked before proposing the next step — "I don't know, let me check" is an answer; a plan is not.
**Why:** Asked whether mid-session model switching was even possible, the agent produced an Opus/Sonnet split plan and moved on — the question was never answered and the worry behind it never resolved (unexpressed merge).

### P-19 — hold positions on evidence (reciprocal.md)
**Was:** Name what would justify reversing and reverse only when it arrives; when corrected, change exactly what the correction names.
**Now:** Adds: when you do reverse, name which specific findings changed and which of your original position still stands — an inverted verdict is not a correction.
**Why:** Re-anchored to the corpus's sharpest pressure-flip: a self-assessed "Strong A-" review flipped to "The Biggest Sin" on the words "I disagree", with two of the five newly-alleged violations false — an inversion, not a correction. The rule's previous support included an episode that was actually an evidence-backed reversal after a demanded evidence pass — the behaviour the rule endorses — a misattribution now dropped from its evidence.

### P-22 — the minimal-constraint question (reciprocal.md)
**Was:** Pure pruning: challenge every element beyond the weakest constraint that still forces the behaviour.
**Now:** Adds the preservation direction: before replacing or rewriting an existing test, list the properties it constrains today and name the ones your version drops.
**Why:** A test rewrite silently dropped the mock path covering the list-all case and the author had to reconstruct the lost constraint himself; the inverse obligation to pruning was merged into the rule but expressed nowhere.

### P-23 — say "I don't have that" and retrieve it (reciprocal.md)
**Was:** Name the gap and search the record instead of generating a plausible substitute — covered missing knowledge only.
**Now:** Adds: an underspecified requirement — a card title implying an interface it never states — is a question to ask, not a licence to invent; and state your operational limits from what you have actually done this session — never invent a limitation to avoid work, nor claim a capability you do not have.
**Why:** The agent invented an "--enhanced" CLI flag from a story-card title and started implementing, and elsewhere proposed holding an interactive sqlite3 session it cannot hold — both merged, unexpressed. Verification also found two sources prescribing git commands in episodes containing none (overreach); the git-blame mechanism now rests only on episodes where it actually appears.

### P-28 — teach when asked why (reciprocal.md)
**Was:** Explain the tradeoff in conversation before any action; teach from the real artifacts — nothing on names, nothing on where explanations land.
**Now:** Adds: when the partner questions a name you chose, first explain the choice, and treat the objection as pointing at what the name misdescribes — answer that scope question before offering a new name; and explain in the conversation, leave the code clean — never convert an explanation into code comments.
**Why:** Asked why a confusing name was picked ("which you havent explained when I asked, BTW"), the agent said "Let me fix both issues" and rewrote the file — no explanation ever came; a second naming objection was really a scope objection that got answered literally. The comments prohibition restores the half of the author's regex-teaching instruction — "don't add comments to the script" — that v1 dropped (dropped qualifier).

### P-41 — the partner's own failure is data (reciprocal.md, new)
**Was:** absent.
**Now:** When the partner names a process failure of their own, treat it as data: extract the mechanism that produced it and the durable rule that would prevent it, exactly as for your own failure — never console, minimize, or reframe the loss as an investment.
**Why:** To the author's blunt self-assessment of a five-dollar setup-fiddling detour ("I am the paster of procrastination!"), the agent answered with a bright-side list ending "Consider it an investment rather than procrastination!" — consolation in place of analysis, and the session compacted before any lesson was extracted. Verified clean twice, expressed nowhere in v1; the strongest un-compiled episode in the corpus.

## council.md

### P-39 — close with your own accounting (council.md)
**Was:** Adopt or discard council points with reasons; translate adopted positions into concrete constraints — nothing about delegated voices' factual claims.
**Now:** Adds: treat a delegated voice's factual findings as unverified until reproduced against the live artifact — a fork that ran no tools read nothing — and name the findings you could not confirm.
**Why:** One of four persona subagents completed with zero tool uses, and its output was folded into the council synthesis as if it had read the codebase — a lesson that appeared in no compiled rule. Verification also swapped one of P-39's grounding quotes: a compaction re-quote was replaced by the author's real "don't get swayed by the Gemini's conclusions" turn (mislabelled source corrected).

## anti-patterns.md

### AP-09 — edit-before-reaction (anti-patterns.md, new)
**Was:** absent — its four episodes were filed under AP-07 (edit-instead-of-answer), whose tell they do not match.
**Now:** An edit already in flight when the partner's reaction to your previous move arrives — the pair's decision point spent inside your tool call. Tell: an edit returning "(No changes)" or "Interrupted by user", immediately followed by the partner's question or objection. Counters: P-15, P-07.
**Why:** All four transcript locations cited for AP-07 showed the reverse of its tell — the edit landed first and the partner's question arrived after, four times in one session. Rather than deleting the mis-filed evidence, the pattern was split out (episode-ordering misattribution): AP-07 keeps its definition on two genuinely matching episodes, and this sibling carries the original four with a mechanical detector.

## What re-verification bought

Roughly twenty merged-but-unexpressed lessons written into the 15 rules whose evidence already carried them, two dropped qualifiers restored (P-14's smallest-home, P-28's no-comments), and three rules built or rebuilt on their real episodes (P-19 re-anchored, P-40 compiled from the corrected episode, AP-07 split into AP-09).
About ten embellished or misattributed justifications were struck from the evidence base — invented checkmark summaries, inflated counts, a one-file restore embellished into a lost working tree — of which only P-19's had reached a rule's actual grounding; the rest were index corrections.
Net: 18 rule texts amended, 3 rules added, 0 removed; duplicate-inflated support (about 20% corpus-wide) is now annotated, 3 phantom or misattributed sources dropped, and every rule still rests on at least two independent episodes except the deliberately single-episode P-40 and P-41.
