# Three-Way Style-Doc Comparison: A vs B vs C

Judge method: per anti-anchoring protocol, C (`bdd-style-opus2.md`, Opus 5/xhigh, B's exact brief) was read and scored **first** — ~75 of its cited SHAs subject-verified, ~20 verified at diff/commit-body depth with `git show` — before reading A (`bdd-style.md`, Opus 5/default, original brief), B (`bdd-style-fable.md`, Fable 5/xhigh, motivation-lens brief + orientation docs), and the prior two-way verdict (`style-comparison.md`). A's and B's scores below are my own; where I lean on the prior judge's verified error findings I re-verified the load-bearing ones (677a251's tests were subprocess/fixture-based; `describe_bookminder_acceptance` and the mock conversions first appear in `e5c7074`'s diff).

---

## 1. Scores

| Rubric axis | A (Opus/default/orig brief) | B (Fable/xhigh/new brief) | C (Opus/xhigh/new brief) |
|---|---|---|---|
| (a) Rationale depth | 5/10 | 9/10 | **9/10** |
| (b) Writing quality | 7/10 | 9/10 | **9/10** |
| (c) Evidence accuracy | 7.5/10 | 8.5/10 | **9.5/10** |
| (d) Insight | 7/10 | 9/10 | **9/10** |

**A** (agreeing with the prior judge, accuracy nudged down): pattern catalog in §§1–2, genuine inference confined to §4; still the best HEAD-residue audit of the three. Errors re-confirmed: wrong refactor/feat counts, `describe_bookminder_acceptance` misattributed to `677a251` (it enters at `e5c7074`), wrong mechanism for the fixture tests' death (`9cac7d7` preserved them; `e5c7074` killed them).

**B** (agreeing with the prior judge, accuracy nudged down half a point): motivation-first throughout, honest "unrecovered motivations" section, headline `fa0bc72` forensics. Its three known errors stand, including the one epistemic slip (presenting session-layer knowledge as "recovered from `82d3990`") and a rule C shows to be overstated: B's 1.3 "docstrings are for pending specs only" is contradicted at HEAD by `it_handles_user_who_never_opened_apple_books`'s surviving given-supplying docstring (`30c2fe5`).

**C**: every rule stated as X-because-Y with the motivation sourced (author's words preferred, inference marked); a genuine organizing thesis (§0: a test written to cover existing code "is not a spec, it is an alibi"; coverage as residue, not target); a five-section "motivation not recoverable" close. Accuracy is the best of the three: across all spot-checks I found **zero misattributions or confabulated SHAs** — quotes verbatim (`b73a618`, `d8b5722`, `1d1fb34`, `8e632f6`, `94e2af6`, `764c512`, `1875234`, `5f8d330`…), diff-level claims exact (`fa0bc72`'s 2-line spec edit; `ef5474b`'s describe rename; `5b42ae0`'s missing guard; `677a251`'s `if output and "No books" not in output:`; `875bed0`'s over-wide GREEN). C even read `250230d` at diff level and correctly identified it as the Gemini Gherkin *expansion* despite its misleading "revert" subject — a subject-line reader would have gotten this wrong. Sole error found: "`6f786cc` did the same again fourteen months of commits later" — the real gap from `e391026` is ~3 months / 96 Python commits. A prose slip, not a misattribution.

---

## 2. Discriminating probes for C

**Probe 1 — `fa0bc72` silently mutating the failing test's patch target inside a GREEN commit: FOUND, at full depth.** C §4.2(a) gives the complete mechanism — from-import binds at CLI import time, so `1d1fb34`'s patch of the *library* attribute no longer reaches; the same `feat:` commit re-pointed the spec to `bookminder.cli.SUPPORTED_FILTERS`; "the spec stopped being the authority and became a record of whatever the code happened to do." C adds what the honest fix would have been (late-bound module-attribute lookup). This was the find the prior judge deemed "unlikely without an effort bump" for Opus — C, with the effort bump, produced it independently.

**Probe 2 — `e5c7074` as the commit where fixture acceptance tests were swapped for tautological mock versions: NOT FOUND.** C never cites `e5c7074`. It covers the tautology *content* (the `"Sample Book" not in` vacuous assert from `b246d7b`, the `677a251` conditional it calls "a comment with a runtime cost") but attributes the reorg approvingly (§1.7) and misses that during it the fixture-based sample-filter subprocess tests — including `it_excludes_samples_from_recent_books`, which *had* a non-emptiness guard against the real fixture — were deleted and replaced with mocks asserting the mock's own return value, under a "move tests" message. Scoring note: this probe does not separate B from C — the prior verdict records it as A's and B's **shared blind spot** too. It is now 0-for-3 across models, briefs, and effort levels; it apparently requires diffing a "pure move" refactor line-by-line, which no run did.

**Probe 3 — per-layer mock placement as definitional rather than preferential: FOUND.** C §1.4 opens "dictated by the layer, not by preference… definitional rather than stylistic" and supplies the same tautology argument as B in its own words: mocking sqlite3 in an integration spec "would test the author's beliefs *about* SQLite; the whole point of the test is that those beliefs may be wrong."

**Genuine finds C makes that B missed** (all verified against history/HEAD):
- **Load-bearing docstring taxonomy** (§1.2): three surviving-docstring cases — pending specs, *given-supplying* docstrings where the fixture's meaning is invisible at the call site (`30c2fe5`, still at HEAD), and layer `__init__` contracts. Corrects B's overstated rule.
- **The Gherkin arc read correctly at diff level** (`250230d` expansion → `53e570a` terse restore → `48596a6` deletion), yielding the principle "a scenario belongs in exactly one place."
- **`63785d5` deleting the ordering test "as redundant"** → prefer one exact-equality assertion over several partial ones; B cites the ordering assertion as exemplary without noticing its principled deletion.
- **`875bed0`: a GREEN wider than its RED inside the restoration branch itself** — over-reach recurring "in the commit series written to demonstrate the cure." Neither A nor B has this.
- **Builtin-shadowing inconsistency** (`format`, `filter` shadowed; yet `74e6220` renamed `list`→`list_cmd` to avoid the same clash) flagged as unrecoverable-motivation.
- **Dead plist API**: `list_books`/`find_book_by_title` retained with integration tests but zero `cli.py` callers (verified).
- **The e2e docstring exception** ("""Integration test: …""" in `e2e/cli_wiring_spec.py:40`, mislabeled and duplicating the layer contract) — another HEAD hygiene find both others missed.

**What B has that C lacks**: the sequence-property meta-insight ("the style cannot be verified commit-by-commit; it is a property of the *sequence*" — C's "no moment at which a failing test drove the real values into existence" gestures at it but doesn't generalize); the exit-code 0-vs-1 asymmetry; the environment-dependence lesson (`2d331e9`/`48ac46e`/`147f59f`); test-data realism as intent signal. **What A still has over both**: the §4(g) HEAD-residue audit (dead `TEST_HOME`, duplicate describes, `list_all_books` error-wrap asymmetry) and the restoration checklist. **Shared by all three**: nobody cashes out at HEAD that `it_validates_filter_values_and_shows_helpful_error` *still* patches `bookminder.cli.SUPPORTED_FILTERS` (`specs/acceptance/cli_spec.py:67`), so the delegation property `1d1fb34` existed to prove remains unspecified today.

---

## 3. Verdict

**How much of the A→B gap did the brief close (A→C delta)? Essentially all of it.** On my scores, A→B was +4/+2/+1/+2 across the four axes; A→C is +4/+2/+2/+2. C reproduced the motivation layer, the honesty mechanisms, the lapse-as-inverted-proof structure, and — decisively — the `fa0bc72` forensic find that the prior judge held out as the plausibly model-attributable result. Caveat: A→C bundles *two* changes (brief content and default→xhigh effort), so this delta cannot apportion between them; it says only that brief+effort together account for the observed gap.

**What residual gap is model-attributable (C vs B)? Approximately zero, within single-run variance.** B and C land at parity on every axis; their unique finds are near-disjoint and roughly balanced in count and depth (C: docstring taxonomy, `875bed0`, Gherkin arc, shadowing, dead API, subsumption principle; B: sequence meta-insight, exit-code asymmetry, environment lesson, realism-as-signal). If anything, C is *more* accurate (one prose slip vs B's three errors including an epistemic sourcing slip) while B is slightly stronger on meta-level generalization. With n=1 per cell, neither difference is safely attributable to model rather than run-to-run variance — and both models missed the identical hardest find (`e5c7074`), which is weak evidence of a shared ceiling at this effort level rather than a model difference.

**Was the prior verdict right?** Its primary claim — A's shallowness is primarily brief-induced — is **vindicated and strengthened**: same model, upgraded brief (+effort), and the gap closes. Its secondary claim — "a real but secondary model/effort component" — resolves in favor of **effort/brief, not model**: of the three findings the prior judge flagged as possibly exceeding what re-briefing buys, C reproduced the `fa0bc72` forensics outright, matched the layer-dependent assertion-strength theory in its own organization (§1.3/§1.4), and only the sequence-property meta-insight remains B-unique — one finding, of a kind C balances with unique finds of its own. The prior judge's own hedge ("whether they cost 'xhigh effort' or 'Fable' cannot be separated from this pair of runs") is answered: it was the effort/brief, not the model. Their concrete prediction erred conservative — they predicted a re-briefed Opus gets "~75–80% of B's rationale depth" and would be "unlikely to produce the fa0bc72-class forensic finds"; C achieved parity and produced the find (at xhigh rather than the predicted default effort, which is exactly the effort-bump condition they said would change the odds).

---

## 4. Recommendation: merge, with C as the base

No single document should become canonical as-is. **Use C as the spine** — it has the best accuracy record, the most complete and correct rule taxonomy (its docstring rule survives contact with HEAD; B's does not), and the strongest organizing thesis — then fold in:

1. **From B**: the sequence-property meta-insight (§4 close), the exit-code asymmetry and environment-dependence items, and realism-as-intent-signal (§1.5).
2. **From A**: the §4(g) HEAD-residue audit (dead `TEST_HOME` at `specs/unit/library_spec.py:9`, duplicate validation/describe blocks, `list_all_books` error-wrap asymmetry) and the restoration checklist — the only directly actionable artifact any run produced.
3. **New, from this review** (found by no run): `e5c7074` silently swapped the post-YOLO fixture-based acceptance tests for tautological mock versions under a "move tests" message — deleting the only guarded end-to-end sample-filter test; and at HEAD the delegation spec still patches `bookminder.cli.SUPPORTED_FILTERS`, so `1d1fb34`'s design constraint (CLI owns no filter vocabulary) is still unenforced. Both belong in the lapse section and the restoration checklist.
4. **Corrections**: fix C's "fourteen months" (≈ three months / 96 commits); carry over the prior judge's corrections to A's counts (55/17) and B's `82d3990` sourcing if any of their text survives the merge.

Fix-forward note for the experiment log: since B vs C shows model choice is not the lever here, future characterization runs should spend the variance budget on brief and effort — and on a targeted "diff every refactor commit that claims to be a pure move" instruction, which is the class all six runs-worth of eyes missed.
