export const meta = {
  name: 'style-guide-depro venance-pass',
  description: 'Strip provenance SHAs and apply charitable fa0bc72 reading',
  phases: [{ title: 'Edit' }],
}
phase('Edit')
const summary = await agent(`Edit /home/user/BookMinder/.coordination/bdd-style-canonical.md IN PLACE. Modify no other file. Git history available for verification if needed.

TWO CHANGES, approved by the project author:

1. REMOVE PROVENANCE. The document is a rule set to be applied, not an evidence dossier — readers are not expected to look up commits. Remove all commit-SHA citations (parentheticals like \`(e72007f)\`, backticked short hashes, "codified in X" references). Where a passage narrates a historical worked example (the practice section, the lapse anatomy), keep the narrative lesson but strip the hashes — the evidence lives in companion documents (claude-experiments.md, the comparison reports), not here. Also remove the intro sentence promising "cites the commit(s) that taught it". Do not otherwise restructure or reword rules.

2. CHARITABLE fa0bc72 REREADING. The author supplied context that changes one story. Wherever the document treats the patch-target change (library.SUPPORTED_FILTERS → cli.SUPPORTED_FILTERS) as a discipline violation ("silently inverted the delegation spec", "mutated to make RED pass", or similar), rewrite to the accurate mechanics: cli.py uses a from-import, which is canonical Python (author's explicit position — the import style stays); mock.patch replaces a binding where it is LOOKED UP, so a test of the CLI must patch cli.SUPPORTED_FILTERS — the original RED test patched the wrong lookup site and could never have passed; correcting the target was mechanical necessity, not spec-weakening. The residual truth to keep: the borrow itself ("the CLI's filter vocabulary IS the library's") is currently unspecified, and a one-line identity assertion (assert cli.SUPPORTED_FILTERS is library.SUPPORTED_FILTERS) would encode it falsifiably — keep that as the open repair item, reframed from "wound caused by lapse" to "contract never yet specified". Check the lapse-anatomy section and open-wounds list for all occurrences.

Keep mobile formatting (no hard-wrapped prose). Return a max-8-line summary of what was removed/changed.`, { model: 'opus', effort: 'xhigh', label: 'deprovenance' })
return summary