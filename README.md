# Nova Light Firmware Repository

This repository contains the `nova-light` ESP-IDF firmware project for the ESP32 family. It is set up for collaborative delivery with humans and coding agents, using a template-first workflow with GitHub Actions, component-oriented architecture, OTA-ready partitioning, lightweight backlog management, and human-gated hardware-in-the-loop validation.

## Starting assumptions

- Framework: ESP-IDF.
- Initial release targets: `esp32-esp-wroom-32` (`esp32`) and `esp32-s3-pico` (`esp32s3`).
- Future ESP32 variants are supported as target classes when platform mapping is added.
- Languages: C and C++.
- Architecture: component-based firmware with a Board Abstraction Layer.
- Connectivity: Wi-Fi, BLE, Ethernet, MQTT, HTTP, and DALI-ready abstractions.
- OTA: A/B OTA baseline with explicit partition table.
- Configuration: `sdkconfig.defaults` plus component-level `Kconfig` files.
- Agent mode: balanced autonomy with safety gates.
- Documentation language: English.

## First local commands

```bash
idf.py set-target esp32
idf.py build
```

## Repository contract

All contributors must read `AGENTS.md` before making changes. Scoped instructions exist in selected subdirectories and must be followed when working there.
