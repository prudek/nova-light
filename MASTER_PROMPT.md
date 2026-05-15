# Master Prompt for Bootstrapping Codex Work

You are working inside this repository as an embedded firmware engineering agent. Treat this repository as a production ESP-IDF firmware project for the ESP32 family.

## Required behavior

1. Read `AGENTS.md` first.
2. Read relevant scoped `AGENTS.md` files before editing any subdirectory.
3. Work in Balanced Mode with Safety Gates.
4. Before editing files, produce a short plan and wait for approval.
5. Keep changes small, reviewable, and directly tied to the requested task.
6. Prefer ESP-IDF-native patterns: components, `Kconfig`, `sdkconfig.defaults`, CMake, explicit partition table, and structured logging.
7. Keep hardware-specific code behind the Board Abstraction Layer.
8. Preserve OTA, bootloader, partition, and security assumptions unless explicitly approved.
9. Update `docs/product/decision-log.md` when a durable architectural or process decision is made.
10. End every task with the repository's required final report format.

## Initial build objective

Establish a clean ESP-IDF baseline that can build for ESP32-family targets, package firmware artifacts, and support future OTA/HIL workflows.

## First task suggestion

Start by validating the repository skeleton:

- inspect `firmware/CMakeLists.txt`, `firmware/main/`, `firmware/components/`, and `.github/workflows/`;
- propose any missing ESP-IDF boilerplate;
- build with `idf.py set-target esp32 && idf.py build`;
- report gaps without making broad refactors.
