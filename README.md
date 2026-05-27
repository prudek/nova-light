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

## Build Firmware Locally

```bash
idf.py -C firmware set-target esp32
idf.py -C firmware build
idf.py -C firmware set-target esp32s3
idf.py -C firmware build
```

Before push/PR updates, run the required local preflight:

```bash
python tools/ci/local_preflight.py
```

## Install via Web Uploader

Use the hosted installer page for `esp32-esp-wroom-32` and `esp32-s3-pico`:

- https://prudek.github.io/nova-light/

If Web Serial is unavailable, use the manual `.bin` download links from the same page.

## Release Quick Start

```bash
python tools/release/cli.py prepare --bump patch
python tools/release/cli.py publish
```

The release workflow publishes merged `.bin` assets for:

- `esp32-esp-wroom-32`
- `esp32-s3-pico`

The firmware uploader page is generated from `web/` and deployed automatically after successful release workflows.

## Repository contract

All contributors must read `AGENTS.md` before making changes. Scoped instructions exist in selected subdirectories and must be followed when working there.
