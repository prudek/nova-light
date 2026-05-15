import hashlib, json, sys
from pathlib import Path

build_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('firmware/build')
version_file = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('VERSION')
version = version_file.read_text(encoding='utf-8').strip() if version_file.exists() else '0.0.0-dev'

artifacts = []
for p in sorted(build_dir.rglob('*.bin')):
    data = p.read_bytes()
    artifacts.append({
        'path': str(p.relative_to(build_dir)),
        'size': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
    })

print(json.dumps({'version': version, 'artifacts': artifacts}, indent=2))
