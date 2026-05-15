# Firmware Architecture

The firmware is organized as ESP-IDF components. Hardware-specific behavior is isolated behind the Board Abstraction Layer. Application logic consumes stable interfaces and must not directly depend on board pins or peripheral electrical details.

## Layers

1. Application orchestration
2. Product logic
3. Connectivity services
4. OTA and storage services
5. Board Abstraction Layer
6. Low-level drivers
