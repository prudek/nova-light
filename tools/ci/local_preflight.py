#!/usr/bin/env python3
"""Local firmware preflight build for supported release targets.

Run this after activating an ESP-IDF environment where `idf.py` is available
on PATH.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_checked(cmd: list[str]) -> None:
    print(f"[preflight] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def resolve_idf_command() -> list[str] | None:
    idf_bat = shutil.which("idf.py.bat")
    if idf_bat is not None:
        return [idf_bat]

    idf_exe = shutil.which("idf.py")
    if idf_exe is not None:
        return [idf_exe]

    idf_path = Path.cwd() / "tools" / "idf.py"
    if "IDF_PATH" in os.environ:
        idf_path = Path(os.environ["IDF_PATH"]) / "tools" / "idf.py"
    if idf_path.exists():
        return [sys.executable, str(idf_path)]

    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Run local ESP-IDF preflight builds.")
    parser.add_argument(
        "--project-dir",
        default="firmware",
        help="Path to ESP-IDF project directory (default: firmware).",
    )
    parser.add_argument(
        "--targets",
        nargs="+",
        default=["esp32", "esp32s3"],
        help="Target list to verify (default: esp32 esp32s3).",
    )
    args = parser.parse_args()

    idf_cmd = resolve_idf_command()
    if idf_cmd is None:
        print(
            "ERROR: idf.py was not found. Activate ESP-IDF first "
            "(export.sh/export.ps1/export.bat).",
            file=sys.stderr,
        )
        return 2

    project_dir = Path(args.project_dir).resolve()
    if not project_dir.exists():
        print(f"ERROR: project directory does not exist: {project_dir}", file=sys.stderr)
        return 2

    run_checked([*idf_cmd, "--version"])
    for target in args.targets:
        print(f"[preflight] Verifying target: {target}")
        run_checked([*idf_cmd, "-C", str(project_dir), "set-target", target])
        run_checked([*idf_cmd, "-C", str(project_dir), "build"])

    print("[preflight] SUCCESS: all targets built successfully.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"[preflight] FAILED: command exited with {exc.returncode}.", file=sys.stderr)
        raise SystemExit(exc.returncode)
