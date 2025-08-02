# Filtering Pipeline Design for xs

## Status: DRAFT - Needs Review

## Problem Statement
Current range selection happens before filtering, making it impossible to get "last N search results". 
Example: `./xs e583 -S "pattern" -5` searches only within the last 5 events, not the last 5 matches.

## Proposed Solution: Clear Pipeline Order

```
Load → Filter → Order → Slice → Display
```

### 1. Load Phase
- Parse JSONL
- Assign sequence numbers

### 2. Filter Phase (reduce the set)
- `--jq 'expression'` - Arbitrary JSON filtering
- `-i/--include` - Include patterns
- `-x/--exclude` - Exclude patterns  
- `-S/--search` - Text search
- All filters are AND'ed together

### 3. Order Phase
- Default: chronological (by sequence)
- Future: `--sort timestamp|size|...`

### 4. Slice Phase (select subset)
- Positional args: `10`, `1-20`, `50+` (current behavior)
- `--head N` - First N of filtered results (NEW)
- `--tail N` - Last N of filtered results (NEW)
- Conflicts: Can't use positional + head/tail

### 5. Display Phase
- Format: `--full`, `--truncated`, (default compact)
- Output: `--json`, `--jsonl`, (default timeline)

## Examples

```bash
# Get last compaction event in full
./xs e583 --jq 'select(.isCompactSummary == true)' --tail 1 --full

# Get last 5 TodoWrite calls
./xs e583 -i TodoWrite --tail 5

# Search in last 100 events (current behavior preserved)
./xs e583 -100 -S "pattern"

# Search all, show last 5 results (new behavior) 
./xs e583 -S "pattern" --tail 5

# ERROR: Conflicting range selectors
./xs e583 -10 --tail 5  # Should error!
```

## Design Principles
1. Clear precedence: Positional args OR head/tail, not both
2. Filters compose: All filters AND together  
3. Display is independent: Any filtered set can be shown in any format
4. Backward compatibility: Current positional behavior unchanged

## Implementation Notes
- Need to refactor filter application order
- Add pipeline stage tracking for debugging
- Clear error messages for conflicts
- Consider streaming for large datasets

## Open Questions
- Should `--tail` buffer all results (memory) or require reverse iteration?
- How to handle `--tail` with streaming output like `--jsonl`?
- Should we add `--limit N` as alias for `--head N`?