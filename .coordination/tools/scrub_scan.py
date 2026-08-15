#!/usr/bin/env python3
"""Secret scan for session transcripts before they are committed to the public repo.

Usage: scrub_scan.py <file-or-dir>... — scans text files for credential-shaped content.
Prints file:line + masked match per hit; exit 1 if any hit, 0 when clean.
A hit is a finding to review with the author, not proof — mask or drop the line, never rewrite silently.
"""

import re
import sys
from pathlib import Path

PATTERNS = [
    ("github-token", re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{20,})")),
    ("github-fine-grained", re.compile(r"\b(github_pat_[A-Za-z0-9_]{20,})")),
    ("aws-access-key", re.compile(r"\b(AKIA[0-9A-Z]{16})\b")),
    ("aws-secret", re.compile(r"aws_secret_access_key\s*[=:]\s*(\S{20,})", re.I)),
    ("anthropic-key", re.compile(r"\b(sk-ant-[A-Za-z0-9-]{20,})")),
    ("openai-key", re.compile(r"\b(sk-[A-Za-z0-9]{32,})")),
    ("slack-token", re.compile(r"\b(xox[baprs]-[A-Za-z0-9-]{10,})")),
    ("private-key-block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("bearer-header", re.compile(r"Authorization:\s*Bearer\s+([A-Za-z0-9._\-]{16,})", re.I)),
    ("basic-auth-url", re.compile(r"https?://[^/\s:]+:([^@\s]{6,})@")),
    ("generic-assignment", re.compile(r"\b(?:api[_-]?key|token|secret|password|passwd)\b\s*[=:]\s*['\"]([^'\"\s]{12,})['\"]", re.I)),
    ("jwt", re.compile(r"\b(eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})")),
    ("netrc-or-pgpass", re.compile(r"\bmachine\s+\S+\s+login\s+\S+\s+password\s+(\S+)", re.I)),
]

SKIP_SUFFIXES = {".sqlite", ".png", ".jpg", ".jpeg", ".epub", ".zip", ".gz"}


def mask(value: str) -> str:
    return value[:6] + "…" + value[-3:] if len(value) > 12 else value[:3] + "…"


def scan_file(path: Path) -> int:
    hits = 0
    try:
        text = path.read_text(errors="replace")
    except OSError as e:
        print(f"# unreadable {path}: {e}", file=sys.stderr)
        return 0
    for lineno, line in enumerate(text.splitlines(), 1):
        for name, pattern in PATTERNS:
            for m in pattern.finditer(line):
                secret = m.group(1) if m.groups() else m.group(0)
                print(f"{path}:{lineno}\t{name}\t{mask(secret)}")
                hits += 1
    return hits


def main(argv: list[str]) -> int:
    if not argv:
        sys.exit(__doc__)
    total = 0
    for arg in argv:
        root = Path(arg)
        files = [root] if root.is_file() else [p for p in sorted(root.rglob("*")) if p.is_file()]
        for f in files:
            if f.suffix.lower() in SKIP_SUFFIXES:
                continue
            total += scan_file(f)
    print(f"# {total} finding(s)", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
