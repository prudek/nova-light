from pathlib import Path
    version = Path('VERSION').read_text(encoding='utf-8').strip() if Path('VERSION').exists() else '0.0.0-dev'
    print(f"# Release notes for {version}
")
    print("Generated release notes placeholder. Replace or extend with conventional commit parsing.")
