# Firmware Agent Instructions

Before changing firmware, read `docs/architecture/firmware-architecture.md`, `docs/architecture/task-model.md`, and `docs/product/requirements.md`.

## ESP-IDF rules

- Prefer componentized design.
- Put public headers in `include/`.
- Put implementation in `src/`.
- Use component-level `Kconfig` for configurable features.
- Keep board-specific behavior inside `components/board`.
- Update `docs/architecture/component-boundaries.md` when adding or moving component responsibilities.
