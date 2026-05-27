#!/usr/bin/env python3
from __future__ import annotations

import json
import sys


def main() -> int:
    if len(sys.argv) != 7:
        print(
            "Usage: make_web_manifest.py <version> <idf_target> <platform_label> <chip_family> <bin_url> <output_path>",
            file=sys.stderr,
        )
        return 2

    version = sys.argv[1]
    idf_target = sys.argv[2]
    platform_label = sys.argv[3]
    chip_family = sys.argv[4]
    bin_url = sys.argv[5]
    output_path = sys.argv[6]

    manifest = {
        "name": "nova-light",
        "version": version,
        "idf_target": idf_target,
        "platform_label": platform_label,
        "new_install_prompt_erase": True,
        "builds": [
            {
                "chipFamily": chip_family,
                "parts": [{"path": bin_url, "offset": 0}],
            }
        ],
    }

    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
