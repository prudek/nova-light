#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHANGELOG_FILE = ROOT / "CHANGELOG.md"
VERSION_FILE = ROOT / "VERSION"

SECTION_RE = re.compile(r"^## \[(?P<label>[^\]]+)\](?: - .+)?$")


def resolve_version(argv: list[str]) -> str:
    if len(argv) > 1 and argv[1].strip():
        return argv[1].strip()
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def extract_section(lines: list[str], version: str) -> list[str]:
    start = None
    end = len(lines)
    for idx, line in enumerate(lines):
        match = SECTION_RE.match(line.strip())
        if match is None:
            continue
        if match.group("label") == version:
            start = idx
            continue
        if start is not None and idx > start:
            end = idx
            break

    if start is None:
        raise RuntimeError(f"Version [{version}] section not found in CHANGELOG.md")

    section = lines[start:end]
    while section and not section[0].strip():
        section = section[1:]
    while section and not section[-1].strip():
        section = section[:-1]
    return section


def main() -> int:
    version = resolve_version(sys.argv)
    lines = CHANGELOG_FILE.read_text(encoding="utf-8").splitlines()
    section = extract_section(lines, version)

    print(f"# Release v{version}")
    print()
    for line in section:
        print(line)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as err:
        print(f"[release-notes] ERROR: {err}", file=sys.stderr)
        raise SystemExit(1)
