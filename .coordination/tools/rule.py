#!/usr/bin/env python3
"""Query mining-corpus YAMLs by rule/gem id. Usage: rule.py <id> [<id>...]; prints each full entry as YAML."""

import sys
from pathlib import Path

import yaml

CORPUS = [Path(".coordination/mining/v2"), Path(".coordination/mining/pairing")]
ID_KEYS = ("rule_id", "gem_id", "id")


def entries(doc):
    if isinstance(doc, dict):
        for key, val in doc.items():
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, dict) and any(k in item for k in ID_KEYS):
                        yield key, item


def main(ids):
    found = set()
    for d in CORPUS:
        for f in sorted(d.glob("*.yaml")):
            try:
                doc = yaml.safe_load(f.read_text())
            except yaml.YAMLError as e:
                print(f"# parse error in {f}: {e}", file=sys.stderr)
                continue
            for section, item in entries(doc):
                item_id = next((item[k] for k in ID_KEYS if k in item), None)
                if item_id in ids:
                    found.add(item_id)
                    print(f"# {f} :: {section}")
                    print(yaml.dump(item, sort_keys=False, allow_unicode=True, width=120))
    missing = set(ids) - found
    if missing:
        print(f"# NOT FOUND: {', '.join(sorted(missing))}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(set(sys.argv[1:])))
