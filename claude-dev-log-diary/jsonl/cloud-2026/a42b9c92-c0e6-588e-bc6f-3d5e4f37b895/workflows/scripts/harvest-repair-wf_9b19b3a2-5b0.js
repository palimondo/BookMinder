export const meta = {
  name: 'harvest-repair',
  description: 'Repair 11 residual schema violations in mining harvest',
  phases: [{ title: 'Repair' }],
}
phase('Repair')
const r = await agent(`Run: /home/user/BookMinder/.venv/bin/python /home/user/BookMinder/.coordination/tools/validate_mining.py /home/user/BookMinder/.coordination/mining/v2/*.yaml — it reports ~11 violations across ~7 files. Fix EVERY violation in place:
- "quote NOT verbatim in source": open the cited source transcript (claude-dev-log-diary/day-NNN.md or scratchpad shard mining/v2/shards for day-020-sN with line-number prefixes), locate the passage via the loc field, and either (a) correct the quote to true verbatim text, or (b) if the text was actually the miner's paraphrase or contains stage-direction annotations like [Edit file], move the descriptive part out of the quote (into what_happened/statement) and retag the provenance field to user-paraphrase/agent-synthesis as appropriate — never leave non-verbatim text labeled as quote.
- "quote exceeds 3 lines": trim to the ≤3 most load-bearing lines (verbatim, use … for elision).
Re-run the validator until ALL files report OK. Then commit: git -C /home/user/BookMinder add (each fixed file by name) && commit -m "docs: repair harvest schema violations (verbatim/provenance fixes)" && push (retry with pull --rebase if rejected).
Return: list of fixes as file:field → what was wrong (verbatim-error vs mislabeled-paraphrase vs overlength), max 12 lines.`, { model: 'opus', effort: 'xhigh', label: 'repair' })
return r