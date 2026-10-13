"""Offline checkpoint list/source/check commands. Never launches a host application."""
import argparse
import ast
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "Content/Python"))
import week07_lessons


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["list", "show", "check"])
    parser.add_argument("id", nargs="?")
    args = parser.parse_args()
    if args.command == "show":
        if args.id is None:
            parser.error("show requires a checkpoint ID, for example UE02")
        print(week07_lessons.source(args.id))
    else:
        steps = week07_lessons.catalog()
        for step in steps:
            if args.command == "check":
                ast.parse(week07_lessons.source(step["id"]), filename=step["file"])
                actual = week07_lessons.blocks(step["id"])
                if list(actual) != step["blocks"]:
                    raise ValueError("Block metadata mismatch: " + step["id"])
                for code in actual.values():
                    ast.parse(code)
            else:
                print(f"{step['id']} [{step['host']}] {step['title']}\n  {step['file']}")
        if args.command == "check":
            print(f"{len(steps)} complete files and their source blocks parse. No host execution performed.")


if __name__ == "__main__":
    main()
