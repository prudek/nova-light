import sys
from pathlib import Path


def _resolve_version() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1].strip()
    version_file = Path("VERSION")
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    return "0.0.0-dev"


def main() -> None:
    version = _resolve_version()
    print(f"# Release notes for {version}")
    print()
    print("Generated release notes placeholder. Replace or extend with conventional commit parsing.")


if __name__ == "__main__":
    main()
