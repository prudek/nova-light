#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path


def _download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "nova-light-pages-builder"})
    with urllib.request.urlopen(request) as response:
        destination.write_bytes(response.read())


def _rewrite_manifest_to_local_bin(manifest_path: Path, bin_name: str) -> None:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    builds = data.get("builds", [])
    if builds and isinstance(builds, list):
        parts = builds[0].get("parts", [])
        if parts and isinstance(parts, list):
            parts[0]["path"] = bin_name
    manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "Usage: materialize_pages_assets.py <releases_api_json> <release_index_json> <site_dist_dir>",
            file=sys.stderr,
        )
        return 2

    releases_api_path = Path(sys.argv[1])
    release_index_path = Path(sys.argv[2])
    site_dist_dir = Path(sys.argv[3])

    releases_api = json.loads(releases_api_path.read_text(encoding="utf-8-sig"))
    index = json.loads(release_index_path.read_text(encoding="utf-8"))
    latest = index.get("latest")
    if not latest:
        return 0

    latest_tag = latest["tag"]
    release = next(
        (
            item
            for item in releases_api
            if item.get("tag_name") == latest_tag and not item.get("draft") and not item.get("prerelease")
        ),
        None,
    )
    if not release:
        return 0

    asset_urls = {asset["name"]: asset["browser_download_url"] for asset in release.get("assets", [])}
    release_asset_dir = site_dist_dir / "assets" / latest_tag
    release_asset_dir.mkdir(parents=True, exist_ok=True)

    latest_platforms = latest.get("platforms", {})
    for platform_id, platform in latest_platforms.items():
        merged_bin_name = platform.get("merged_bin_name")
        manifest_name = f"manifest-{platform_id}.json"
        if merged_bin_name in asset_urls:
            _download(asset_urls[merged_bin_name], release_asset_dir / merged_bin_name)
        if manifest_name in asset_urls:
            _download(asset_urls[manifest_name], release_asset_dir / manifest_name)
            _rewrite_manifest_to_local_bin(release_asset_dir / manifest_name, merged_bin_name)

    for optional_name in ("manifest.json", f"checksums-{latest_tag}.txt"):
        if optional_name in asset_urls:
            _download(asset_urls[optional_name], release_asset_dir / optional_name)

    local_prefix = f"./assets/{latest_tag}"

    def patch_release_entry(entry: dict) -> None:
        if entry.get("tag") != latest_tag:
            return
        for platform_id, platform in entry.get("platforms", {}).items():
            merged_bin_name = platform.get("merged_bin_name")
            manifest_name = f"manifest-{platform_id}.json"
            if merged_bin_name:
                platform["merged_bin_url"] = f"{local_prefix}/{merged_bin_name}"
            platform["web_manifest_url"] = f"{local_prefix}/{manifest_name}"
        entry["release_manifest_url"] = f"{local_prefix}/manifest.json"
        entry["checksums_url"] = f"{local_prefix}/checksums-{latest_tag}.txt"

    patch_release_entry(index["latest"])
    for item in index.get("releases", []):
        patch_release_entry(item)

    release_index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
