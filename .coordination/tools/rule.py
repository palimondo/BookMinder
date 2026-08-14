#!/usr/bin/env python3
"""Provenance toolkit for the mining corpus and compiled skills.

Usage:
  rule.py <corpus-id>...                      print the raw YAML fragment(s), verbatim source lines with file:line header
  rule.py -c [N] <corpus-id>...               also print transcript windows around every day-NNN:LNNN reference in the
                                              fragment (N context lines each side, default 60), with line numbers
  rule.py -r <compiled-id>... [-c [N]]        resolve compiled rule ids (T-NN / P-NN / B-NN / AP-NN / INV-*) to their
                                              corpus sources via .coordination/compile/rule-index-*.md, then as above

Corpus ids look like d019-R2, p020s1-R9, p021-R8, d006-R15. Run from the repo root.
The transcript windows are the verification substrate: judge quote fidelity, episode fidelity, and generalization
against these, never against the YAML summary alone.
"""

import re
import sys
from pathlib import Path

CORPUS_DIRS = [Path(".coordination/mining/v2"), Path(".coordination/mining/pairing")]
RULE_INDEX_GLOB = ".coordination/compile/rule-index-*.md"
DIARY = Path("claude-dev-log-diary")
ID_LINE = re.compile(r"^\s*-\s+(?:rule_id|gem_id|id):\s*(\S+)\s*$")
CORPUS_ID = re.compile(r"\b[dp]\d{3}[a-z0-9]*-R\d+\b")
LOC_REF = re.compile(r"(day-\d{3})[a-z0-9-]*:L(\d+)(?:\s*[-–]\s*L?(\d+))?")


def find_fragments(wanted):
    found = {}
    for d in CORPUS_DIRS:
        for f in sorted(d.glob("*.yaml")):
            lines = f.read_text(errors="replace").splitlines()
            starts = [(i, m.group(1)) for i, line in enumerate(lines) if (m := ID_LINE.match(line))]
            for pos, (i, item_id) in enumerate(starts):
                if item_id not in wanted or item_id in found:
                    continue
                end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
                while end > i and not lines[end - 1].strip():
                    end -= 1
                found[item_id] = (f, i, lines[i:end])
    return found


def resolve_compiled(rids):
    corpus_ids, seen_rows = [], []
    for f in sorted(Path(".").glob(RULE_INDEX_GLOB)):
        for line in f.read_text(errors="replace").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and cells[0] in rids:
                seen_rows.append(cells[0])
                corpus_ids += CORPUS_ID.findall(line)
    for rid in rids:
        if rid not in seen_rows:
            print(f"# NOT IN ANY RULE-INDEX: {rid}", file=sys.stderr)
    return corpus_ids


def print_transcript_windows(text, ctx):
    for day, start, end in {m.groups() for m in LOC_REF.finditer(text)}:
        start, end = int(start), int(end or start)
        day_file = DIARY / f"{day}.md"
        if not day_file.exists():
            print(f"## {day}.md NOT FOUND for L{start}")
            continue
        lines = day_file.read_text(errors="replace").splitlines()
        lo, hi = max(0, start - 1 - ctx), min(len(lines), end + ctx)
        print(f"## {day_file}:L{lo + 1}-L{hi} (cited: L{start}{f'-L{end}' if end != start else ''})")
        for n in range(lo, hi):
            marker = ">" if start <= n + 1 <= end else " "
            print(f"{marker}{n + 1}\t{lines[n]}")
        print()


def main(argv):
    ctx, want_ctx, resolve, ids = 60, False, False, []
    it = iter(argv)
    for a in it:
        if a == "-c":
            want_ctx = True
        elif a == "-r":
            resolve = True
        elif a.isdigit() and want_ctx:
            ctx = int(a)
        else:
            ids.append(a)
    if not ids:
        sys.exit(__doc__)
    if resolve:
        ids = resolve_compiled(set(ids)) or ids
    fragments = find_fragments(set(ids))
    for item_id in ids:
        if item_id not in fragments:
            print(f"# NOT FOUND IN CORPUS: {item_id}", file=sys.stderr)
            continue
        f, i, frag = fragments[item_id]
        print(f"# ===== {item_id} @ {f}:L{i + 1}")
        print("\n".join(frag))
        print()
        if want_ctx:
            print_transcript_windows("\n".join(frag), ctx)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
