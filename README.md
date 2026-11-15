# Sofle Keyboard Firmware

This repository contains the ZMK firmware for the Sofle keyboard.

## Features

- Split keyboard design
- OLED displays
- RGB backlighting
- Wireless connectivity via Bluetooth

## Key coordinates

Name physical keys `Lrc` or `Rrc`: `L`/`R` selects the left/right half,
`r` is the row counted upward from the thumbs, and `c` is the column counted
outward from the center. Both numbers start at 1. Coordinates stay attached
to physical keys when their layer bindings change.

- Row 1: thumb keys; row 2: bottom letter row; row 3: home row;
  row 4: top letter row; row 5: number row.
- Letter rows have six columns per half; thumb rows have five.
  Encoder and pointing controls are separate from this numbering.
- `R31` is H; `R13` is the original dash key; `L11` is the innermost
  left thumb key.

| Physical key | Main | Secondary | Test | Studio position (zero based) |
|---|---|---|---|---|
| `L36` | Escape | Caps Lock | Escape (inherited) | 26 |
| `L11` | Delete | Delete (inherited) | Hyper modifiers | 57 |
| `R13` | Tap dash / hold Secondary | Delete | Tap dash / hold Secondary (inherited) | 61 |

Hold `R13` to access Secondary. These names are physical coordinates; ZMK
matrix coordinates and Studio positions use their own numbering.

## Main-layer shortcuts

- `L36`: plain Escape, with no hold behavior.
- `L11`: plain Delete.
- Top-left key: `~` (US layout), with no hold modifier.

## Optional Test layer

Hold **R13 (right dash/action)** and tap **T (L41)** to toggle Test on or off.
The same chord is available while Test is on. Test is off at startup.

Test changes only **L11** to a normal Hyper modifier key: Control + Option +
Shift + Command. It uses `&kp LC(LS(LA(LGUI)))` directly in ZMK, with no Mac
remapping or tap/hold decision. A tap presses and releases the modifiers;
holding it keeps them down for a shortcut. Every other Test binding is
transparent, including R13 and T, so the exit chord remains reachable.

This source provides five normal layers plus three reserved Studio slots.
The reserved slots have transparent defaults; Studio can add/name/remove
experimental layers within that capacity without another firmware build.
The first firmware update from the previous four-layer version is still needed
to provide this capacity. Keep the first four layer IDs and their order intact.

The Windows and Hardware layers retain their existing bindings. Saved Studio
settings can shadow new source defaults after a firmware update. Back up and
verify the whole keymap, then apply the reviewed repository bindings through
the CLI. Do not use Restore Stock Settings as a routine update step.

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
