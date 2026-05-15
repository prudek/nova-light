from pathlib import Path
required = [Path('AGENTS.md'), Path('README.md'), Path('MASTER_PROMPT.md')]
missing = [str(p) for p in required if not p.exists()]
if missing:
    raise SystemExit(f"Missing required files: {missing}")
print("Markdown structure check passed")
