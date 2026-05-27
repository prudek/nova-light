# Repository Agent Instructions

## Operating mode

Work in **Balanced Mode with Safety Gates**.

The agent may implement normal firmware changes, create components, update tests, update backlog items, and propose documentation updates. The agent must produce a plan first and wait for human approval before editing files.

## Mandatory first-read context

Before any non-trivial change, read:

1. `README.md`
2. `docs/product/product-brief.md`
3. `docs/product/requirements.md`
4. `docs/architecture/firmware-architecture.md`
5. The nearest scoped `AGENTS.md` file for the area being changed

## Safety gates

The agent may propose but must explicitly call out and obtain human approval before changing:

- `firmware/sdkconfig.defaults`
- `firmware/partitions.csv`
- OTA flow or firmware rollback behavior
- Secure Boot, Flash Encryption, certificate handling, or secrets handling
- Hardware assumptions, pin mappings, power assumptions, boot strapping pins, or peripheral electrical behavior
- Public APIs between components
- CI/CD release semantics

## Required work pattern

For every task:

1. Restate the task and assumptions.
2. Identify touched areas and scoped instructions.
3. Produce an implementation plan.
4. Wait for approval before editing.
5. Make the smallest coherent change set.
6. Run or describe verification.
7. Update docs/backlog/decision log when durable project knowledge changes.
8. Finish with a concise report.

Before pushing code or opening/updating a PR, run local preflight verification in an activated ESP-IDF environment:

```bash
python tools/ci/local_preflight.py
```

The command must pass for both `esp32` and `esp32s3`. This rule is environment-agnostic and applies on Windows, Linux, and macOS.

## Final report format

```markdown
## Summary
## Files changed
## Verification
## Risks / assumptions
## Decision log updates
## Suggested next steps
```

## Coding constraints

- Prefer deterministic, testable modules.
- Keep hardware access behind the Board Abstraction Layer.
- Avoid hidden global state where practical.
- Use explicit timeouts for blocking operations.
- Check and propagate ESP-IDF error codes.
- Avoid unbounded dynamic allocation in long-running production paths.
- Avoid blocking delays in production FreeRTOS tasks unless justified.
- Do not hardcode secrets, credentials, certificates, keys, Wi-Fi passwords, or tokens.

## Documentation rules

- Documentation is written in English.
- Architectural changes require `docs/product/decision-log.md` updates.
- Repeated human feedback that changes the way the agent should work should be captured in `AGENTS.md` or a scoped `AGENTS.md`.
- Every pull request prepared by the agent must include a `CHANGELOG.md` update under `## [Unreleased]` before merge/release preparation.

## Backlog rules

- Lightweight backlog items live under `backlog/`.
- If technical debt is discovered, the agent may create a task in `backlog/tasks/` using YAML front matter.
- Do not inflate the backlog with trivial cleanup items.

## Branch and PR naming

- When creating branches or pull requests, use the `prudek` prefix.
- Do not use the `codex` prefix for branch or PR naming.
