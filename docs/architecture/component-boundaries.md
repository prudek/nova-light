# Component Boundaries

Each component should expose a small public API under `include/`. Internal implementation details stay in `src/`.

`console_cli` owns the minimal UART shell baseline (`help`, `version`, `ping`) used for bring-up and release smoke checks.
