#!/usr/bin/env python3
"""
Write RUNNER_TEMP/sa.json from GOOGLE_APPLICATION_CREDENTIALS_JSON (GitHub Actions).
Avoids bash heredoc / YAML indentation issues.
"""

import json
import os
import pathlib
import sys


def main():
    raw = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON", "")
    if not raw.strip():
        print("ERROR: GOOGLE_APPLICATION_CREDENTIALS_JSON is empty or missing", file=sys.stderr)
        return 1
    runner_temp = os.environ.get("RUNNER_TEMP", "")
    if not runner_temp:
        print("ERROR: RUNNER_TEMP is not set", file=sys.stderr)
        return 1
    path = pathlib.Path(runner_temp) / "sa.json"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print("ERROR: GOOGLE_APPLICATION_CREDENTIALS_JSON is not valid JSON: %s" % e, file=sys.stderr)
        return 1
    path.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    print("Wrote %s (keys: %s)" % (path, list(data.keys())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
