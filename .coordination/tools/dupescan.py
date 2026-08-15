import hashlib
import sys
from collections import defaultdict
from pathlib import Path

# Shingling runs over a whitespace-collapsed TOKEN stream, not over lines, so that
# two renderings of the same console output match even when the terminal re-wrapped
# them at different widths. Line numbers are recovered from each token's origin line.
K = 100          # shingle size in substantive tokens
MIN_RUN = 150    # report merged runs of at least this many tokens (~30 diary lines)
MAX_REPEAT = 60  # skip boilerplate shingles occurring more often than this
GLYPHS = "│╭╮╰╯─┃|"

diary = Path("/home/user/BookMinder/claude-dev-log-diary")
files = sorted(diary.glob("day-*.md"))

kept = {}  # file -> list of (orig_lineno, token_hash)
for f in files:
    rows = []
    for i, line in enumerate(f.read_text(errors="replace").splitlines(), 1):
        for token in line.split():
            norm = token.strip(GLYPHS)
            if norm:
                rows.append((i, hashlib.md5(norm.encode()).hexdigest()[:8]))
    kept[f.name] = rows

shingles = defaultdict(list)  # shingle hash -> [(file, token_idx)]
for name, rows in kept.items():
    for idx in range(len(rows) - K + 1):
        sh = hashlib.md5("".join(h for _, h in rows[idx:idx + K]).encode()).hexdigest()[:16]
        shingles[sh].append((name, idx))

capped = 0
pair_hits = defaultdict(set)  # (fileA, fileB) -> set of (idxA, idxB)
for locs in shingles.values():
    if len(locs) < 2:
        continue
    if len(locs) > MAX_REPEAT:
        capped += 1
        continue
    for a in range(len(locs)):
        for b in range(a + 1, len(locs)):
            (fa, ia), (fb, ib) = locs[a], locs[b]
            if fa == fb and abs(ia - ib) < K:
                continue
            pair_hits[(fa, fb)].add((ia, ib))

results = []
for (fa, fb), hits in pair_hits.items():
    used = set()
    for ia, ib in sorted(hits):
        if (ia, ib) in used:
            continue
        run = 0
        while (ia + run + 1, ib + run + 1) in hits:
            used.add((ia + run + 1, ib + run + 1))
            run += 1
        length = run + K
        if length >= MIN_RUN:
            a_start = kept[fa][ia][0]
            a_end = kept[fa][min(ia + length - 1, len(kept[fa]) - 1)][0]
            b_start = kept[fb][ib][0]
            b_end = kept[fb][min(ib + length - 1, len(kept[fb]) - 1)][0]
            results.append((length, fa, a_start, a_end, fb, b_start, b_end))

results.sort(reverse=True)
top = int(sys.argv[1]) if len(sys.argv) > 1 else 25
print(f"{len(results)} duplicated regions (>= {MIN_RUN} substantive tokens); "
      f"{capped} boilerplate shingles skipped (>{MAX_REPEAT} occurrences):")
for length, fa, a1, a2, fb, b1, b2 in results[:top]:
    kind = "WITHIN-FILE" if fa == fb else "CROSS-FILE"
    print(f"{kind}: {length:6d} tok  {fa}:L{a1}-L{a2}  <->  {fb}:L{b1}-L{b2}")
