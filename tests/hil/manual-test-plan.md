# Manual HIL Test Plan

## Preconditions
- Test rig available.
- Target board identified.
- Firmware artifact and manifest available.

## Basic smoke test
1. Flash bootloader, partition table, and application image.
2. Capture serial log.
3. Confirm boot banner.
4. Confirm no watchdog reset.
5. Record firmware version and board variant.
