# Sofle Keyboard Firmware

This repository contains the ZMK firmware for the Sofle keyboard.

## Features

- Split keyboard design
- OLED displays
- RGB backlighting
- Wireless connectivity via Bluetooth

## Main-layer shortcuts

- Escape: tap for Esc; hold for Right Control after 200 ms, or immediately when
  another key is pressed. Vorssaint maps Right Control to Super
  (Control + Option + Shift + Command), with no separate tap action.
- Top-left key: `~` (US layout), with no hold modifier.

The Windows layer retains its existing bindings. If ZMK Studio has saved runtime
keymap changes, use its **Restore Stock Settings** action after flashing to adopt
these firmware defaults.

## Entering Bluetooth firmware-update mode

On the Hardware layer, press the physical **Z** key for the left half or **/** key
for the right half. Each binding resets only its own half into the Adafruit
nRF52 bootloader's legacy Bluetooth DFU mode (`GPREGRET = 0xa8`). The other half
keeps running. These bindings require this firmware to be installed first.
Install the matching firmware on both halves before using right-half OTA entry.

Update one half at a time using its matching firmware. Keep the other half out
of DFU mode so that an updater cannot accidentally select it. This configuration
keeps the existing application address (`0x26000`) and bootloader; it does not
upgrade the bootloader or Nordic SoftDevice.

The OTA packages target the legacy Adafruit DFU protocol, device type `0x0052`,
and **S140 6.1.1** SoftDevice firmware ID `0x00b6`. These are package prerequisites,
not a claim that the connected keyboard has that SoftDevice. Verify each half's
bootloader/SoftDevice and preserve its `INFO_UF2.TXT` and `CURRENT.UF2` before the
initial USB installation. Do not use the `settings_reset` image as an update.

Each successful GitHub firmware build publishes the normal `firmware` UF2
artifact and separate `ota-left-s140-6.1.1` / `ota-right-s140-6.1.1` artifacts.
Each OTA artifact contains that half's DFU ZIP, prerequisites, source revision,
and checksum. Use these ZIPs only after confirming the installed SoftDevice
matches; they are not USB-flashable UF2 files.

## Update List

- 2024/12/21
  1. Added support for zmk-studio (just refresh the left hand to use).
- 2024/10/24
  1. Modified power supply mode to reduce power consumption.
  2. Fixed the automatic shut-off feature for RGB power supply.

> If your keyboard was updated before October 24, please update to the latest firmware.

---

## Contact Me

For 3D printed model files or any issues and malfunctions with the keyboard, please contact 380465425@qq.com

## Sofle Keymap

<img src="keymap-drawer/dark/eyelash_sofle.svg" >

[Light mode version](keymap-drawer/light/eyelash_sofle.svg)
