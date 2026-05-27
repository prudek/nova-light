# Development Setup

Install ESP-IDF, clone the repo, enter `firmware/`, set the target, and build.

## Quick Local Validation

Run this from the repository root before the first build:

```bash
idf.py --version
cd firmware
idf.py set-target esp32
idf.py build
```

If `idf.py` is not found, initialize your ESP-IDF environment first (for example by sourcing `export.sh` on Linux/macOS or running `export.bat`/`export.ps1` on Windows in your ESP-IDF installation).

## Required Pre-Push Verification

After activating your ESP-IDF environment, run:

```bash
python tools/ci/local_preflight.py
```

This verifies the release targets (`esp32`, `esp32s3`) locally before push/PR updates.

## Local Release Commands

Use these commands for semantic releases:

```bash
python tools/release/cli.py prepare --bump patch
python tools/release/cli.py publish
```

`prepare` includes the same local preflight gate and refuses to continue on a dirty git state.
