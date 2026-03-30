#!/usr/bin/env python3
"""Run sync_push then gsc_report (or subcommands). Suitable for CI and local."""

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script, extra):
    cmd = [sys.executable, str(HERE / script)] + extra
    print("+", " ".join(cmd))
    return subprocess.call(cmd)


def main():
    parser = argparse.ArgumentParser(description="SEO automation runner")
    parser.add_argument(
        "command",
        nargs="?",
        default="all",
        choices=("all", "push", "gsc"),
        help="Which step to run (default all)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args, passthrough = parser.parse_known_args()
    extra = ["--dry-run"] if args.dry_run else []

    if args.command in ("all", "push"):
        code = run("sync_push.py", extra)
        if code != 0:
            return code

    # Pass through extra args (e.g. --days 14) only to gsc_report
    if args.command in ("all", "gsc"):
        code = run("gsc_report.py", extra + passthrough)
        if code != 0:
            return code

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
