#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PLATFORMS = (
    {
        "id": "esp32-esp-wroom-32",
        "label": "ESP32 / ESP-WROOM-32",
        "idf_target": "esp32",
        "chip_family": "ESP32",
    },
    {
        "id": "esp32-s3-pico",
        "label": "ESP32-S3-PICO",
        "idf_target": "esp32s3",
        "chip_family": "ESP32-S3",
    },
)

VERSION_RE = re.compile(r"^v(\d+\.\d+\.\d+)$")


def parse_release(release: dict) -> dict | None:
    if release.get("draft") or release.get("prerelease"):
        return None

    tag = str(release.get("tag_name", "")).strip()
    match = VERSION_RE.match(tag)
    if match is None:
        return None

    version = match.group(1)
    assets = {asset.get("name"): asset.get("browser_download_url") for asset in release.get("assets", [])}

    platform_data = {}
    for platform in PLATFORMS:
        platform_id = platform["id"]
        merged_name = f"nova-light-{platform_id}-v{version}.bin"
        manifest_name = f"manifest-{platform_id}.json"
        platform_data[platform_id] = {
            "platform_id": platform_id,
            "label": platform["label"],
            "idf_target": platform["idf_target"],
            "chip_family": platform["chip_family"],
            "merged_bin_name": merged_name,
            "merged_bin_url": assets.get(merged_name),
            "web_manifest_url": assets.get(manifest_name),
        }

    return {
        "tag": tag,
        "version": version,
        "name": release.get("name") or f"nova-light v{version}",
        "published_at": release.get("published_at"),
        "html_url": release.get("html_url"),
        "body": release.get("body") or "",
        "platforms": platform_data,
        "release_manifest_url": assets.get("manifest.json"),
        "checksums_url": assets.get(f"checksums-v{version}.txt"),
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: generate_release_index.py <releases_json> <output_path>", file=sys.stderr)
        return 2

    releases_json = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    raw = json.loads(releases_json.read_text(encoding="utf-8-sig"))
    releases = []
    for release in raw:
        parsed = parse_release(release)
        if parsed is not None:
            releases.append(parsed)

    index = {
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "platforms": list(PLATFORMS),
        "latest": releases[0] if releases else None,
        "releases": releases,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
