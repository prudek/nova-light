#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 4:
        print(
            "Usage: assemble_release_manifest.py <version> <output_path> <manifest_platform_json...>",
            file=sys.stderr,
        )
        return 2

    version = sys.argv[1]
    output_path = Path(sys.argv[2])
    manifest_paths = [Path(arg) for arg in sys.argv[3:]]

    platforms = []
    for manifest_path in sorted(manifest_paths):
        data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        builds = data.get("builds", [])
        bin_path = None
        if builds and isinstance(builds, list):
            parts = builds[0].get("parts", [])
            if parts and isinstance(parts, list):
                bin_path = parts[0].get("path")
        platforms.append(
            {
                "platform_label": data.get("platform_label"),
                "idf_target": data.get("idf_target"),
                "web_manifest": manifest_path.name,
                "merged_bin": bin_path,
            }
        )

    merged = {
        "name": "nova-light",
        "version": version,
        "platforms": platforms,
    }

    output_path.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
