# Release Process

Release is driven by local CLI commands and a tag-triggered GitHub workflow.

## Local release commands

Run from repository root in an activated ESP-IDF environment:

```bash
python tools/release/cli.py prepare --bump patch
python tools/release/cli.py publish
```

`prepare` performs:

- clean git state validation,
- local preflight (`python tools/ci/local_preflight.py`),
- `VERSION` update,
- `CHANGELOG.md` release section creation,
- release commit + `vX.Y.Z` tag creation.

`publish` pushes the prepared commit and tag to `origin`.

## Published platforms

- `esp32-esp-wroom-32` (`idf.py` target: `esp32`)
- `esp32-s3-pico` (`idf.py` target: `esp32s3`)

## Version validation gate

Release is blocked unless `VERSION` matches the requested release version:

- Tag-triggered release: `GITHUB_REF_NAME=vX.Y.Z` must match `VERSION=X.Y.Z`.
- Manual run: workflow input `version` must match `VERSION`.

## Release artifacts

Each release publishes per-platform merged binaries and manifests:

- `nova-light-esp32-esp-wroom-32-vX.Y.Z.bin`
- `nova-light-esp32-s3-pico-vX.Y.Z.bin`
- `manifest-esp32-esp-wroom-32.json`
- `manifest-esp32-s3-pico.json`
- `manifest.json` (combined platform manifest)
- `checksums-vX.Y.Z.txt`

## GitHub Pages deployment

After each published GitHub release, the Pages workflow rebuilds a static firmware installer site.

Site features:

- Web Serial firmware install button (ESP Web Tools),
- platform selector for both product platforms,
- manual `.bin` download links,
- changelog rendered from release notes.
