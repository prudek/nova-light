# Firmware Versioning

The repository uses `VERSION` as the human-owned firmware version source.

## Release policy

- Release tags must follow `vX.Y.Z`.
- `VERSION` must be exactly `X.Y.Z` for tag `vX.Y.Z`.
- Manual release workflow input `version` must also match `VERSION`.

If the values do not match, the release workflow fails before build starts.
