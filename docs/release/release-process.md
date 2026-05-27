# Release Process

Release can be triggered manually through GitHub Actions or by pushing a semantic version tag.

## Published platforms

- `esp32-esp-wroom-32` (`idf.py` target: `esp32`)
- `esp32-s3-pico` (`idf.py` target: `esp32s3`)

## Version validation gate

Release is blocked unless `VERSION` matches the requested release version:

- Tag-triggered release: `GITHUB_REF_NAME=vX.Y.Z` must match `VERSION=X.Y.Z`.
- Manual release: workflow input `version` must match `VERSION`.

## Release artifacts

Each platform produces a separate artifact bundle:

- `firmware-release-<platform_label>-v<version>`

Bundle contents include bootloader, partition table, application binaries, ELF/MAP files, `manifest.json`, and `release-notes.md`.
