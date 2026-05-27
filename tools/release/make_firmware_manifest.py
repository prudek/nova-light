import hashlib
import json
import sys
from pathlib import Path


def _read_version(version_file: Path) -> str:
    if version_file.exists():
        return version_file.read_text(encoding="utf-8").strip()
    return "0.0.0-dev"


def main() -> None:
    build_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("firmware/build")
    version_file = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("VERSION")
    idf_target = sys.argv[3] if len(sys.argv) > 3 else "unknown"
    platform_label = sys.argv[4] if len(sys.argv) > 4 else idf_target

    artifacts = []
    for path in sorted(build_dir.rglob("*.bin")):
        data = path.read_bytes()
        artifacts.append(
            {
                "path": str(path.relative_to(build_dir)),
                "size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )

    manifest = {
        "version": _read_version(version_file),
        "idf_target": idf_target,
        "platform_label": platform_label,
        "artifacts": artifacts,
    }
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
