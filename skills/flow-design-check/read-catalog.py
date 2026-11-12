#!/usr/bin/env python3
"""Read titles by category or complete entries by exact id."""

import argparse
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    titles = modes.add_parser("titles")
    titles.add_argument("prefixes", nargs="+")
    titles.add_argument("--match", help="Case-insensitive text in the title or body")
    entries = modes.add_parser("entries")
    entries.add_argument("ids", nargs="+")
    args = parser.parse_args()

    lines = Path(__file__).with_name("ANTIPATTERNS.md").read_text(encoding="utf-8").splitlines()
    catalog = {}
    for position, line in enumerate(lines):
        heading = re.match(r"^### ([A-Z]{2}-[0-9]{2}) ", line)
        if heading:
            catalog[heading[1]] = lines[position : position + 5]

    if args.mode == "entries":
        unknown = set(args.ids) - catalog.keys()
        if unknown:
            entries.error("Unknown entry IDs: " + ", ".join(sorted(unknown)))
        print("\n\n".join("\n".join(catalog[id_]) for id_ in dict.fromkeys(args.ids)))
        return

    prefixes = set(args.prefixes)
    unknown = prefixes - {id_[:2] for id_ in catalog}
    if unknown:
        titles.error("Unknown category prefixes: " + ", ".join(sorted(unknown)))
    cue = args.match.casefold() if args.match else ""
    for id_, entry in catalog.items():
        if id_[:2] in prefixes and any(cue in line.casefold() for line in entry):
            print(entry[0])


if __name__ == "__main__":
    main()
