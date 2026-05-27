# Firmware Versioning

The repository uses `VERSION` as the human-owned firmware version source.

## Release command behavior

- `python tools/release/cli.py prepare` is the authoritative local release entrypoint.
- If `VERSION` is `X.Y.Z-dev`, `prepare` promotes it to `X.Y.Z` by default.
- `prepare --bump patch|minor|major` increments the current stable version.
- `prepare --version X.Y.Z` sets an explicit release version.

## Release policy

- Release tags must follow `vX.Y.Z`.
- `VERSION` must be exactly `X.Y.Z` for tag `vX.Y.Z`.
- Manual release workflow input `version` must also match `VERSION`.

If the values do not match, the release workflow fails before build starts.
