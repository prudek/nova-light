# Agent Review Checklist

- Confirm repository-level and scoped `AGENTS.md` instructions were followed.
- Verify safety-gated areas were not changed without explicit approval.
- Verify docs were updated when durable process or architecture changed.
- Verify CI workflow changes include clear failure messages and safe defaults.
- Verify release/versioning changes remain consistent with `VERSION`.
- Verify local preflight was executed in an active ESP-IDF environment with `python tools/ci/local_preflight.py` before push/PR updates.
