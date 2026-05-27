# Decision Log

## ADR-0001: Use ESP-IDF as the baseline framework

Status: accepted

Reason: ESP-IDF provides first-party support for ESP32-family devices, components, CMake, Kconfig, OTA, and production-oriented tooling.

## ADR-0002: Use component-level Kconfig

Status: accepted

Reason: Component-level Kconfig keeps feature flags and tunables close to each component while preserving ESP-IDF-native configuration workflows.

## ADR-0003: Publish release artifacts per product platform

Status: accepted

Reason: Product release bundles are now explicitly published for `esp32-esp-wroom-32` and `esp32-s3-pico`, with version/tag consistency checks and per-platform manifest metadata for traceability.
