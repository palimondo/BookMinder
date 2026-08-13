import hashlib
import sys
from collections import defaultdict
from pathlib import Path

K = 20          # shingle size in kept lines
MIN_RUN = 30    # report merged runs of at least this many kept lines

diary = Path("/home/user/BookMinder/claude-dev-log-diary")
files = sorted(diary.glob("day-*.md"))

kept = {}  # file -> list of (orig_lineno, hash)
for f in files:
    rows = []
    for i, line in enumerate(f.read_text(errors="replace").splitlines(), 1):
        norm = "".join(line.split())
        norm = norm.strip("│╭╮╰╯─┃|")
        if len(norm) > 15:
            rows.append((i, hashlib.md5(norm.encode()).hexdigest()[:12]))
    kept[f.name] = rows

shingles = defaultdict(list)  # shingle hash -> [(file, kept_idx)]
for name, rows in kept.items():
    for idx in range(len(rows) - K + 1):
        sh = hashlib.md5("".join(h for _, h in rows[idx:idx + K]).encode()).hexdigest()[:16]
        shingles[sh].append((name, idx))

pair_hits = defaultdict(set)  # (fileA, fileB) -> set of (idxA, idxB)
for locs in shingles.values():
    if len(locs) < 2:
        continue
    for a in range(len(locs)):
        for b in range(a + 1, len(locs)):
            (fa, ia), (fb, ib) = locs[a], locs[b]
            if fa == fb and abs(ia - ib) < K:
                continue
            pair_hits[(fa, fb)].add((ia, ib))

results = []
for (fa, fb), hits in pair_hits.items():
    hits = sorted(hits)
    used = set()
    for ia, ib in hits:
        if (ia, ib) in used:
            continue
        run = 0
        while (ia + run + 1, ib + run + 1) in pair_hits[(fa, fb)]:
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
print(f"{len(results)} duplicated regions (>= {MIN_RUN} substantive lines):")
for length, fa, a1, a2, fb, b1, b2 in results[:25]:
    kind = "WITHIN-FILE" if fa == fb else "CROSS-FILE"
    print(f"{kind}: {length:5d} lines  {fa}:L{a1}-L{a2}  <->  {fb}:L{b1}-L{b2}")
