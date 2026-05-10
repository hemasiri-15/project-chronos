#!/usr/bin/env python3
"""
main.py — Project Chronos CLI
Author: Hema Siri Guduru (SE24UCSE043), Mahindra University
Powered by: Google Gemini API

Usage:
    python main.py "fragment text"
    python main.py --verbose "fragment text"
    python main.py --output report.json "fragment text"
    python main.py --batch fragments.txt
    python main.py --json "fragment text"
"""

import argparse
import json
import sys
from pathlib import Path

from src.chronos_engine import ChronosEngine


BANNER = r"""
  ██████╗██╗  ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ███████╗
 ██╔════╝██║  ██║██╔══██╗██╔═══██╗████╗  ██║██╔═══██╗██╔════╝
 ██║     ███████║██████╔╝██║   ██║██╔██╗ ██║██║   ██║███████╗
 ██║     ██╔══██║██╔══██╗██║   ██║██║╚██╗██║██║   ██║╚════██║
 ╚██████╗██║  ██║██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝███████║
  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
  AI Archaeological Engine · Mahindra University · SE24UCSE043
  Powered by Google Gemini 2.0 Flash
"""

LINE = "─" * 62


def print_result(result, verbose: bool = False):
    print(BANNER)
    print(f"  ERA         {result.era}")
    print(f"  PLATFORM    {result.platform}")
    bar = "█" * (result.confidence // 10) + "░" * (10 - result.confidence // 10)
    print(f"  CONFIDENCE  {bar}  {result.confidence}%")
    print(LINE)

    print("\n  RECONSTRUCTION\n")
    for line in result.reconstruction.split(". "):
        if line.strip():
            print(f"    {line.strip()}.")

    print(f"\n{LINE}")
    print(f"\n  SLANG GLOSSARY  ({len(result.slang)} terms)\n")
    for s in result.slang:
        print(f"    [{s.term}]  →  {s.meaning}")

    if verbose:
        print(f"\n{LINE}")
        print(f"\n  CULTURAL CONTEXT\n")
        # Word-wrap at 58 chars
        words = result.context.split()
        line_buf, lines = [], []
        for w in words:
            line_buf.append(w)
            if len(" ".join(line_buf)) > 58:
                lines.append("    " + " ".join(line_buf[:-1]))
                line_buf = [w]
        if line_buf:
            lines.append("    " + " ".join(line_buf))
        print("\n".join(lines))

    print(f"\n{LINE}")
    print(f"\n  SOURCES\n")
    for src in result.sources:
        print(f"    • {src.title}")
        print(f"      {src.url}")

    print(f"\n{LINE}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Project Chronos — AI Archaeological Engine (Gemini)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               '  python main.py "smh at the top 8 drama. g2g ttyl"\n'
               '  python main.py --verbose "asl? brb 10 mins"\n'
               '  python main.py --output report.json "no cap fr fr"',
    )
    parser.add_argument("fragment", nargs="?", help="Text fragment to analyze")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show cultural context")
    parser.add_argument("--output", "-o", metavar="FILE", help="Save JSON report to file")
    parser.add_argument("--batch", metavar="FILE", help="Analyze all lines in a text file")
    parser.add_argument("--json", action="store_true", dest="json_only",
                        help="Output JSON only (machine-readable, no banner)")
    parser.add_argument("--api-key", metavar="KEY", help="Gemini API key (overrides .env)")
    args = parser.parse_args()

    try:
        engine = ChronosEngine(api_key=args.api_key or None)
    except ValueError as e:
        print(f"\n  ⚠  {e}\n")
        sys.exit(1)

    # ── Batch mode ────────────────────────────────────────────────
    if args.batch:
        path = Path(args.batch)
        if not path.exists():
            print(f"\n  ⚠  File not found: {args.batch}\n")
            sys.exit(1)
        fragments = [l.strip() for l in path.read_text().splitlines() if l.strip()]
        print(f"\n  Processing {len(fragments)} fragments...\n")
        results = engine.analyze_batch(fragments)
        for i, (frag, result) in enumerate(zip(fragments, results), 1):
            print(f"\n{'='*62}")
            print(f"  Fragment {i}: {frag[:55]}{'...' if len(frag) > 55 else ''}")
            if result:
                print_result(result, args.verbose)
                if args.output:
                    out_path = Path(args.output).stem + f"_{i}.json"
                    Path(out_path).write_text(result.to_json())
                    print(f"  Saved → {out_path}")
            else:
                print("  ⚠  Analysis failed for this fragment.\n")
        return

    # ── Single fragment ───────────────────────────────────────────
    fragment = args.fragment
    if not fragment:
        parser.print_help()
        sys.exit(0)

    try:
        result = engine.analyze(fragment)
    except (ValueError, RuntimeError) as e:
        print(f"\n  ⚠  Analysis failed: {e}\n")
        sys.exit(1)

    if args.json_only:
        print(result.to_json())
    else:
        print_result(result, args.verbose)

    if args.output:
        Path(args.output).write_text(result.to_json())
        print(f"  Saved → {args.output}\n")


if __name__ == "__main__":
    main()
