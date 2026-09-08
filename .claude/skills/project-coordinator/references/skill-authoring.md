# Skill authoring — shape by content type, and the failure register

A skill page is read whole by an agent that has already decided to read it, and every token in it is paid on every load. Write it as instructions to that agent, in the imperative with the why attached, and never as a document describing itself to a reviewer. The author reviews pages one at a time on a phone and stops at the first sentence that does not earn its place, so the gates below run before a page is presented, not after.

## Shape follows content type

- **Conduct rules** (how to work, how to behave): numbered entries, each a bold headline that IS the rule, then the why. The headline must be complete on its own.
- **Domain knowledge** (how an external system works): a model organized by the subject's own structure — what exists, what each part holds, when to read which, what is unknown — in prose and short lists under headings. No numbered entries, no headline sentences: over facts they are calorie-free labels.
- **History and motivation**: narrative, because the content is the why; strip register defects but do not manufacture a closing instruction per entry.
- **State, rulings, open decisions**: numbered entries, each opening with what the agent does about it.
- When a page is compiled from a corpus of mined corrections, the corpus is the coverage test, never the outline: build the model first, fold each correction in where it applies, then walk the corpus and confirm each item has a home. Mapping corrections one-to-one into entries produces a page organized by the history of mistakes instead of the shape of the subject.

## The register — each with its test

- **Self-description.** The page talks about itself ("this page compresses…", "the compressed record of…"). Test: does the sentence tell the agent what to do or what is true? If it describes the page, cut it; the router carries the routing.
- **Discovery narration.** How a fact was found, who relayed it, what was corrected when ("the consequence was a decision…", "was observed in a census"). Test: delete the narration; if the fact and its why survive, it was provenance. Provenance lives in commit messages and the record.
- **Stamps and standing doubt.** Verification tags per item, and "unsettled" flags over discrepancies that have an explanation. Test: the only distinction a page carries is known versus unknown; an unknown is stated as a fact about ignorance ("ordering is unknown"), and a resolved discrepancy is not an unknown. The suite is the verification; a page never asks the agent to re-verify per session.
- **Foreign procedure.** Instructions for another activity (census taking, exploration method, recovery steps) inside a knowledge page. Test: would the reader know when to apply it? If it belongs to a task, it lives in that task's brief.
- **Trailing gloss.** A clause that restates the sentence as a code description or aphorism ("which is why X does Y", "…is not a feature"). Test: strip it; if nothing is lost, it was garnish. Do not demand "why it matters to the code" per item in a brief — the why is written only where the rule does not already imply it.
- **Code narration.** Function names, query text, error strings, spec findings restated in a knowledge page. Test: the code is small and read whole before any task; a page states the decisions that constrain the code, never the code.
- **Layer mixing.** Product consequences, rulings, or doc-writing rules attached to a domain fact. Test: would the sentence stay true if the product did not exist? If not, it moves to its layer — settled design decisions, rulings, the editing section, the story card.
- **Row anecdotes.** A field described by enumerating observations exception by exception ("on one row…, on another…", "every row seen so far"). Test: state the positive rule with its validity range; the evidence stays in the record.
- **Scattered pointers.** A "see doc section X" on every item. Test: the page is read whole, so one trailing map from section to items does the job; a pointer stays inline only when it is itself an instruction.
- **Circumlocution.** Paraphrasing around a name to obey a no-mention rule ("the canonical rules file"). Test: name the thing plainly where a fact concerns it; the rule against restating harness-loaded content is not a rule against naming it — use the agent-neutral name.
- **Rot-prone specifics.** Line numbers, sizes, counts, versions, dates, environment sentences ("this environment has no…"). Test: file names only; a count is one command away and the page names the command.
- **Wide tables.** They render as one endless line on a phone. Test: per-item bullets instead.

Run the register over a page before presenting it, and again over every page that shares the defect the author just named: a correction applies everywhere, not to the instance he happened to read.
