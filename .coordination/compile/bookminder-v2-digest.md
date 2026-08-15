# Bookminder skill v2 — review digest (commit ffa7963)

One commit, three pages: 12 existing rules amended, none added, none removed — no verifier retracted a source, so every rule kept faithful support. Where pairing's revision was dominated by restoration, this one is dominated by contraction: domain lore cut back to what the transcripts hold — mechanisms unwelded from unexplained observations, author guesses re-hedged, Gemini-relayed material marked second-hand — plus two dropped negatives restored and one inverted chronology put back in order. A counter-current runs the other way: where a claim's weak source could be replaced by checking the live tree directly, the judge did that instead of hedging, and three claims came out stronger. Unlike pairing, v1 of this skill was never author-reviewed — this digest is the entry point to its revision history, but the actual review object is the full v2 pages, presented separately.

## goals-and-history.md

### B-05 — vehicle and benchmark (goals-and-history.md)
**Was:** "process artifacts are therefore deliverables, not cruft" — unbounded.
**Now:** The deliverable artifacts are enumerated — the story-cards-to-acceptance-tests-to-code chain, the session diary, the agent-instruction files (themselves WIP, their techniques untested, his words) — and AI-written retrospective meta-analysis is explicitly excluded, with the author's standing "AI slop" caveat attached and a cross-reference to B-31.
**Why:** Every source of this rule is a turn where the author affirms the vehicle framing and qualifies it in the same breath — calling most of docs/ "basically just AI slop" and warning the meta-project could end up a big baggage of it; read unbounded (underreach), the rule licensed exactly the artifact inflation he spent a day deleting a dozen documents to undo.

## repo-geography-and-fixtures.md

### B-20 — cheapest grounding (repo-geography-and-fixtures.md)
**Was:** Opened with "read the ~290 lines"; the line-count prohibition stood bare.
**Now:** Opens with: `/hi` (and this skill) already supply the session-start census — read what you were given before running discovery commands of your own; and the prohibition now carries its falsification — both repos vendor a venv in-tree, and the raw counts behind a rejected "44% code reduction" headline were almost entirely site-packages.
**Why:** The rule's cited episode is the author interrupting a run of bash `find` calls to ask why they were needed when `/hi` had already run `tree` — a census-reuse lesson the skill nowhere expressed, which the corpus had converted into a venv-noise tip (embellished-because); the venv evidence is a different session's raw line counts, re-filed here from B-31 where nothing used them.

### B-21 — land mines (repo-geography-and-fixtures.md)
**Was:** A diary grant meant "targeted range reads in the foreground; never whole-file reads, never background-subagent greps" — implying any broad grep is forbidden.
**Now:** Range reads of the named lines, not whole-file ingests — one whole-file read against an explicit line-range grant wasted 10% of context and drew a rebuke — and never from a background subagent, where the author cannot see or stop what is being read; he kills those on sight.
**Why:** The author killed a background Task mid-grep on a diary file, then watched four foreground diary sweeps with the same broad pattern pass without a word — the tested boundary is observability and stoppability, not sweep breadth, so the breadth ban was the corpus's own addition (overreach).

### B-24 — CLI shape (repo-geography-and-fixtures.md)
**Was:** "one repeatable `--filter` option … (`cloud`, `!cloud`, `sample`, `!sample`)" — reading as the whole vocabulary, with "repeatable" untrue at HEAD.
**Now:** One `--filter` option, single-value at HEAD (multiple filters are deferred future work with no story yet); the cloud/sample forms implemented today, reading status (`finished`, `unread`, `in-progress`) already assigned to the same option by the approved plan; no `--flag`, no `--status`, no `--type` — reintroducing one is reopening a settled decision.
**Why:** The plan the author approved folds reading status into `--filter`, and his steer in the same exchange explicitly deferred multiple filters — but compile had dropped the mined rule's operative negative (underreach), leaving `--status finished` looking like a fresh design choice to the next implementer; the judge also struck "repeatable", which the Click declaration at HEAD contradicts.

### B-25 — the Book type (repo-geography-and-fixtures.md)
**Was:** "`path` and `updated` are `NotRequired` because the SQLite path cannot supply them."
**Now:** The type guarantees only what every code path can honestly supply — the DB-backed path fabricates `path` as an empty string; see the domain page's open path-correlation problem.
**Why:** The code at HEAD shows the DB path filling `updated` from `ZLASTOPENDATE` — the old WHY was simply false for that field and inherited B-51's overreach for `path`; the corpus entry behind it was the agent reading its own code, mislabeled as author paraphrase (misattribution) and now relabeled agent-synthesis.

### B-26 — personas and the front-door seam (repo-geography-and-fixtures.md)
**Was:** `never_opened_user` described as "only the OS-created `com.apple.iBooksX` container — no BKAgentService, no plist, no sqlite" — reading as no BKLibrary directory either, collapsing the distinction from `legacy_books_user`.
**Now:** The container holds an empty `BKLibrary` directory and nothing else, and a new sentence states the two error paths the legacy/never-opened split exercises — missing directory and empty directory raise different messages — and why the leaf `.gitkeep` is load-bearing; stated as verified@tree.
**Why:** The detail's only cited source was the third re-log of a Gemini-written day summary that does not even contain it (overreach over relay material); rather than hedge, the judge confirmed it against the fixture trees and the two raise sites in the library code at HEAD — turning the weakest-sourced claim on the page into one of the strongest.

## apple-books-domain.md

### B-41 — plist vs database roles (apple-books-domain.md)
**Was:** "the plist omits cloud-only titles, so absence from the plist proves nothing about library membership"; "`updateDate` in the plist is publisher-revision metadata, not reading activity."
**Now:** Titles the database knew were demonstrably missing from even a freshly converted plist snapshot and the cause was never established — so plist absence proves nothing in either direction; `updateDate` is probably publisher-revision metadata — the author's never-verified hypothesis — and what the episode settled is that the `sort_by='updated'` feature was deleted as YAGNI because the field's meaning was unknown.
**Why:** The first sentence welded a mechanism onto an anomaly whose author verdict was "still a mystery to us. Something's fishy there"; the second flattened a triple-hedged author guess — uncertain, probably, I guess — into schema lore and dropped the only durable decision the episode produced (overreach, dropped hedge).

### B-43 — the ZSTATE census (apple-books-domain.md)
**Was:** "earlier research recorded it as 'Series entity / unowned series book' … but a later systematic re-probe observed 5 only as a second row for a title that already had a 3, which the series story does not predict."
**Now:** Two observations in this order, consistent with each other without settling it: the batch census showing the duplicate row came first; the `ZSERIESID` join came later and was the more systematic probe — the series entity and the unowned member titles sharing one series id, a structure that would also produce exactly that duplicate row — with the entity/member relation left unknown per the author, the ~206-row population named, and the docs' ZTITLE discriminator marked as the agent's own substitute after the author rejected a ZAUTHOR heuristic.
**Why:** Both halves of the old sentence were wrong — the delta's headline fix: the duplicate-row batch precedes the join by a day, and the join supported the author's series hypothesis rather than contradicting it (an inverted chronology; the discriminator a misattribution now indexed agent-synthesis); "the method that produced every real breakthrough" shrank to the one breakthrough the corpus attests.

### B-44 — sample detection (apple-books-domain.md)
**Was:** "Per-title sample observations flipped between probes in 2025 (the same title read `ZISSAMPLE 0` one session and `1` another)" — instability framing; the display/filter divergence clause implicitly carried a reverted-for-lacking-a-spec rationale; the lifecycle stood unattributed.
**Now:** Per-title values are time-varying, not noise — a sample reading cloud-and-unflagged, then local-and-flagged after being opened, is the proposed lifecycle at work, so freshness stamps and re-run queries stay mandatory; the 3-only filter is where the author's revert of an unauthorized widening left it — he never ruled the wider predicate wrong — so change neither side without his direction and a spec; the lifecycle is flagged as reconstructed second-hand in a relayed log analysis, never probed live.
**Why:** The flip the rule called instability is the very lifecycle its previous sentence proposed, and the revert rationale was invented — the author's words were "I didn't stop you in time", a premature-change objection, not a spec ruling (embellished-because); the lifecycle's only source is a Gemini summary the author pasted, mislabeled as his paraphrase (misattribution).

### B-47 — samples and list recent (apple-books-domain.md)
**Was:** Hedged "appears never to populate" but silent on source quality and on a same-session counter-observation.
**Now:** Both claims flagged second-hand — a relayed log summary plus the agent's own requirements reasoning, never a live probe — and the counter-observation carried: the UI renders some cloud samples at 1%, so the untested part is precisely the database-side claim that progress stays 0.0 for samples.
**Why:** Seven hundred lines into the same session the rule is mined from, the agent recorded "Samples can occasionally have progress, contrary to my initial assumption" — a qualifier v1 dropped; and no author turn stands behind any of the rule's cited sources, which carried his-paraphrase labels over Gemini-relay and agent text (misattribution).

### B-51 — path correlation (apple-books-domain.md)
**Was:** Headline "(verified@tree, library.py:73)" over "the database has no usable path."
**Now:** What is verified@tree is the empty-string `path` pending ZASSETID correlation; whether the database has any usable path column was never checked — left as an acknowledged TODO at the author's direction — so "the path exists only in Books.plist" is a needs-live-DB guess, not established schema.
**Why:** The whole transcript basis is the agent's hedged guess that the database might not have path info, and the author's instruction was precisely to record the open question as a FIXME/TODO rather than resolve it; v1 promoted the guess to fact under the strongest stamp the page has (overreach).

### B-53 — docs/apple_books.md epistemic status (apple-books-domain.md)
**Was:** "a running record of guesses" — true but unactionable.
**Now:** Adds that the doc's "Edge Cases" and NULL-handling sections, like its `ZCONTENTTYPE` mapping (B-45), are speculation written in the same voice as its observations.
**Why:** The session that committed the doc had written those sections as pure conjecture — never-observed NULL guards encoded as ready-to-paste SQL, one of which later seeded a real defect in production — and the mined entry named them; compile had generalized the names away (a faithful source more specific than the compiled rule).

## What re-verification bought

Five rules cut back to what the transcripts hold — B-41's two welded mechanisms, B-43's inverted chronology, B-44's invented revert rationale, B-47's and B-51's second-hand guesses re-hedged — and two dropped operative clauses restored (B-24's no-`--status` negative with the reading-status vocabulary, B-20's census-reuse lesson), while B-26, B-25 and B-24 were strengthened by checking the tree directly instead of trusting or hedging their sources.
Underneath, the evidence base was cleaned: eight source clusters relabeled agent-synthesis (Gemini relays, the agent's own code archaeology, miner synthesis over narrower author turns), day-020's re-logged episodes deduplicated so B-24's and B-26's apparent source breadth now matches reality, two mis-filed index rows re-homed, and B-52's uncited clause kept with its real cross-skill sources recorded in the index — no text change, hence no entry above.
Net: 12 rule texts amended, 0 added, 0 removed; no source retracted, so every rule keeps faithful support; twelve author-attested rules are marked corpus-unverified for the next verification era rather than silently trusted.

Separately from this delta: two post-judge, author-directed additions — B-32 (native transcript-backup ritual, repo-geography page) and B-67 (public-by-design, goals page) — postdate the judge pass, are not part of the diff digested here, and need no entries; the v2 pages under review therefore differ from v1 by these 12 amendments plus those two new rules.
