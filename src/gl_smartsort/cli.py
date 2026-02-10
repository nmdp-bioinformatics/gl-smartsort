\
from __future__ import annotations

import sys
import argparse
from .smartsort import smart_sort


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="gl-smartsort",
        description="Smart-sort GL Strings into a canonical order.",
    )
    p.add_argument(
        "gl",
        nargs="?",
        help="GL string. If omitted, reads from stdin (one per line).",
    )
    args = p.parse_args(argv)

    if args.gl is not None:
        sys.stdout.write(smart_sort(args.gl) + "\n")
        return 0

    # stdin mode
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            sys.stdout.write("\n")
            continue
        sys.stdout.write(smart_sort(line) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
