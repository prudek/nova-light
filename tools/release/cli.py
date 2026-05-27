#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION_FILE = ROOT / "VERSION"
CHANGELOG_FILE = ROOT / "CHANGELOG.md"

SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
SEMVER_DEV_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)-dev$")
UNRELEASED_HEADER = "## [Unreleased]"


def run(cmd: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed ({' '.join(cmd)}):\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result.stdout.strip()


def ensure_clean_git_state() -> None:
    status = run(["git", "status", "--porcelain"], cwd=ROOT)
    if status:
        raise RuntimeError("Working tree is not clean. Commit/stash changes before running release prepare.")


def ensure_on_branch() -> str:
    branch = run(["git", "branch", "--show-current"], cwd=ROOT)
    if not branch:
        raise RuntimeError("Detached HEAD is not supported for release prepare.")
    return branch


def read_version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip()


def parse_semver(value: str) -> tuple[int, int, int]:
    match = SEMVER_RE.match(value)
    if not match:
        raise RuntimeError(f"Invalid semantic version: {value}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def parse_semver_or_dev(value: str) -> tuple[int, int, int]:
    pure = SEMVER_RE.match(value)
    if pure:
        return int(pure.group(1)), int(pure.group(2)), int(pure.group(3))
    dev = SEMVER_DEV_RE.match(value)
    if dev:
        return int(dev.group(1)), int(dev.group(2)), int(dev.group(3))
    raise RuntimeError(f"Invalid semantic version: {value}")


def bump_version(current: str, bump: str) -> str:
    major, minor, patch = parse_semver(current)
    if bump == "major":
        return f"{major + 1}.0.0"
    if bump == "minor":
        return f"{major}.{minor + 1}.0"
    if bump == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise RuntimeError(f"Unsupported bump level: {bump}")


def update_changelog_for_release(version: str, release_date: dt.date) -> None:
    text = CHANGELOG_FILE.read_text(encoding="utf-8")
    lines = text.splitlines()

    try:
        unreleased_idx = next(
            i for i, line in enumerate(lines) if line.startswith("## [") and "Unreleased" in line
        )
    except StopIteration as exc:
        raise RuntimeError("CHANGELOG.md does not contain an Unreleased section.") from exc

    next_section_idx = len(lines)
    for i in range(unreleased_idx + 1, len(lines)):
        if lines[i].startswith("## ["):
            next_section_idx = i
            break

    unreleased_body = lines[unreleased_idx + 1 : next_section_idx]
    while unreleased_body and not unreleased_body[0].strip():
        unreleased_body = unreleased_body[1:]
    while unreleased_body and not unreleased_body[-1].strip():
        unreleased_body = unreleased_body[:-1]
    if not unreleased_body:
        unreleased_body = ["### Changed", "- No notable changes recorded."]

    new_release_header = f"## [{version}] - {release_date.isoformat()}"
    new_lines = lines[:unreleased_idx]
    if new_lines and new_lines[-1].strip():
        new_lines.append("")
    new_lines.append(UNRELEASED_HEADER)
    new_lines.append("")
    new_lines.append(new_release_header)
    new_lines.extend(unreleased_body)
    if next_section_idx < len(lines):
        new_lines.append("")
        new_lines.extend(lines[next_section_idx:])
    CHANGELOG_FILE.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8")


def run_local_preflight() -> None:
    python = sys.executable
    run([python, "tools/ci/local_preflight.py"], cwd=ROOT)


def prepare_release(args: argparse.Namespace) -> int:
    ensure_clean_git_state()
    branch = ensure_on_branch()
    print(f"[release] On branch: {branch}")

    print("[release] Running local preflight ...")
    run_local_preflight()

    current = read_version()
    current_base = parse_semver_or_dev(current)
    if args.version:
        target = args.version
    elif current.endswith("-dev"):
        target = f"{current_base[0]}.{current_base[1]}.{current_base[2]}"
    else:
        target = bump_version(current, args.bump)
    parse_semver(target)

    if target == current:
        raise RuntimeError("Target version equals current VERSION. Choose a newer version.")

    tag = f"v{target}"
    existing_tag = run(["git", "tag", "-l", tag], cwd=ROOT)
    if existing_tag.strip():
        raise RuntimeError(f"Tag already exists: {tag}")

    VERSION_FILE.write_text(target + "\n", encoding="utf-8")
    update_changelog_for_release(target, dt.date.today())

    run(["git", "add", "VERSION", "CHANGELOG.md"], cwd=ROOT)
    run(["git", "commit", "-m", f"Release {target}"], cwd=ROOT)
    run(["git", "tag", tag], cwd=ROOT)

    print(f"[release] Prepared release {target}")
    print(f"[release] Created commit and tag {tag}")
    return 0


def publish_release(args: argparse.Namespace) -> int:
    version = read_version()
    parse_semver(version)
    tag = f"v{version}"

    tag_exists = run(["git", "tag", "-l", tag], cwd=ROOT)
    if not tag_exists.strip():
        raise RuntimeError(f"Tag {tag} does not exist. Run prepare first.")

    branch = ensure_on_branch()
    print(f"[release] Publishing branch {branch} and tag {tag} ...")
    run(["git", "push", "origin", branch], cwd=ROOT)
    run(["git", "push", "origin", tag], cwd=ROOT)
    print("[release] Publish complete.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Release management CLI for nova-light.")
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="Prepare release commit and tag.")
    version_mode = prepare.add_mutually_exclusive_group()
    version_mode.add_argument("--bump", choices=["major", "minor", "patch"], default="patch")
    version_mode.add_argument("--version", help="Explicit version (X.Y.Z).")
    prepare.set_defaults(func=prepare_release)

    publish = sub.add_parser("publish", help="Push prepared release branch and tag.")
    publish.set_defaults(func=publish_release)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        return int(args.func(args))
    except RuntimeError as err:
        print(f"[release] ERROR: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
