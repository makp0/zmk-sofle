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
- Top-left key: tap for `~` (US layout); hold for Right Command.

The Windows layer retains its existing bindings. If ZMK Studio has saved runtime
keymap changes, use its **Restore Stock Settings** action after flashing to adopt
these firmware defaults.

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
