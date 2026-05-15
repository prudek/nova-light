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
