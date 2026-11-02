"""Offline demonstration CLI; network access requires explicit opt-in."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from .codex import codex_synthetic_observe
from .library import LibraryError, load_query, load_references
from .matcher import compare
from .review import make_blank_review_sheet

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Synthetic clinical reference library (NOT diagnostic)")
    sub = parser.add_subparsers(dest="command", required=True)
    match = sub.add_parser("match", help="Offline descriptive match to synthetic references")
    match.add_argument("--query", required=True, type=Path)
    match.add_argument("--library", required=True, type=Path)
    match.add_argument("--limit", type=int, default=10)
    sheet = sub.add_parser("review-sheet", help="Generate a blank clinician-owned comparison worksheet")
    sheet.add_argument("--query", required=True, type=Path)
    sheet.add_argument("--library", required=True, type=Path)
    observe = sub.add_parser("codex-observe", help="Codex-only optional synthetic image demo")
    observe.add_argument("--image", type=Path, required=True)
    observe.add_argument("--manifest", type=Path, required=True)
    observe.add_argument("--allow-api", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "match":
            result = compare(load_query(args.query), load_references(args.library), limit=args.limit)
        elif args.command == "review-sheet":
            result = make_blank_review_sheet(load_query(args.query), load_references(args.library))
        else:
            result = codex_synthetic_observe(str(args.image), str(args.manifest), allow_api=args.allow_api)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (LibraryError, ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
if __name__ == "__main__":
    raise SystemExit(main())
