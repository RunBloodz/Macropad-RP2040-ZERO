# 15-Key + 1 Rotary Encoder Macropad (RP2040-Zero & KMK Firmware)

This repository contains the complete firmware code and guide for building a **15-Key + 1 Rotary Encoder (4x4 Matrix) Macropad** driven by Waveshare RP2040-Zero, CircuitPython, and KMK Firmware.

---

## Table of Contents
1. [Overview & Features](#overview--features)
2. [Pinout & Hardware Connections](#pinout--hardware-connections)
3. [4x4 Matrix Layout & Physical Wiring](#4x4-matrix-layout--physical-wiring)
4. [Diode Wiring & Orientation Tutorial](#diode-wiring--orientation-tutorial)
5. [Rotary Encoder Setup](#rotary-encoder-setup)
6. [CircuitPython & KMK Installation](#circuitpython--kmk-installation)
7. [Customizing Keymaps & Macros](#customizing-keymaps--macros)

---

## Overview & Features

- **Microcontroller**: Waveshare RP2040-Zero (RP2040 MCU with 29 GPIOs, USB-C)
- **Matrix**: 4x4 Grid (15 mechanical switches + 1 rotary encoder in top-left position `Row 0, Col 0`)
- **Rotary Encoder**: Incremental EC11 rotary encoder (Pins A/B for rotation, separate push button pin)
- **Firmware Framework**: KMK Firmware running on CircuitPython
- **Features**:
  - Full Anti-Ghosting / NKRO with diode matrix
  - Multi-layer support (Layer 0: Numpad/Media, Layer 1: Shortcuts & Productivity Macros)
  - Customizable Rotary Encoder rotation and click functions per layer
  - No backlight (maximizes power efficiency and simplifies build)

---

## Pinout & Hardware Connections

### RP2040-Zero GPIO Assignment

| Module / Component | Function | RP2040-Zero GPIO Pin | Notes |
| :--- | :--- | :--- | :--- |
| **Matrix Rows** | Row 0 | `GP0` | Top Row |
| | Row 1 | `GP1` | Second Row |
| | Row 2 | `GP2` | Third Row |
| | Row 3 | `GP3` | Bottom Row |
| **Matrix Columns**| Column 0 | `GP4` | Left Column |
| | Column 1 | `GP5` | Second Column |
| | Column 2 | `GP6` | Third Column |
| | Column 3 | `GP7` | Right Column |
| **Rotary Encoder**| Channel A | `GP8` | Rotation pin A |
| | Channel B | `GP9` | Rotation pin B |
| | Switch (Button)| `GP10` | Push button (GND on other side) |
| | Common / GND | `GND` | Ground pin for Encoder |

---

## 4x4 Matrix Layout & Physical Wiring

The 4x4 matrix comprises 16 total grid intersections. **Top-Left intersection (Row 0, Column 0)** is occupied by the physical body of the Rotary Encoder.

```
+-------------------+-------------------+-------------------+-------------------+
|  [ENCODER KNOB]   |  [KEY 1] (R0,C1)  |  [KEY 2] (R0,C2)  |  [KEY 3] (R0,C3)  |
|   (Row 0, Col 0)  |  Slash (/)        |  Asterisk (*)     |  Layer 1 Hold     |
+-------------------+-------------------+-------------------+-------------------+
|  [KEY 4] (R1,C0)  |  [KEY 5] (R1,C1)  |  [KEY 6] (R1,C2)  |  [KEY 7] (R1,C3)  |
|  Numpad 7         |  Numpad 8         |  Numpad 9         |  Minus (-)        |
+-------------------+-------------------+-------------------+-------------------+
|  [KEY 8] (R2,C0)  |  [KEY 9] (R2,C1)  |  [KEY 10] (R2,C2) |  [KEY 11] (R2,C3) |
|  Numpad 4         |  Numpad 5         |  Numpad 6         |  Plus (+)         |
+-------------------+-------------------+-------------------+-------------------+
|  [KEY 12] (R3,C0) |  [KEY 13] (R3,C1) |  [KEY 14] (R3,C2) |  [KEY 15] (R3,C3) |
|  Numpad 1         |  Numpad 2         |  Numpad 3         |  Numpad Enter     |
+-------------------+-------------------+-------------------+-------------------+
```

---

## Diode Wiring & Orientation Tutorial

### Why Use Diodes?
Diodes prevent "ghosting" or "masking" when pressing multiple mechanical keys simultaneously. Recommended diodes: **1N4148** signal diodes (axial or SMD).

### Diode Polarization
Diodes allow current to flow in only one direction:
- **Anode (+)**: Plain body side
- **Cathode (-)**: Side marked with the **black line / stripe**

```
          Anode (+)        Cathode (-)
       +--------------[==|==============]--------------+
                            Black Stripe
```

### Orientation Setup: `COL2ROW` vs `ROW2COL`

Our firmware defaults to `DiodeOrientation.COL2ROW`.

#### 1. `COL2ROW` (Recommended & Default in `code.py`):
- Connect **Anode (+)** to key switch terminal / Column line.
- Connect **Cathode (- stripe side)** directly to the **Row line**.

```
  [Column Pin GP4..GP7]
          |
          |
     [Key Switch]
          |
          |
       (Anode)
       +----+
       | |> |  Diode (1N4148)
       +----+
     (Cathode - Stripe)
          |
          v
    [Row Pin GP0..GP3]
```

#### 2. `ROW2COL`:
If you accidentally solder the diodes in reverse (Cathode pointing to Column):
Change line 32 in `code.py`:
```python
keyboard.diode_orientation = DiodeOrientation.ROW2COL
```

---

## Rotary Encoder Setup

An EC11 rotary encoder has 5 pins:
- **3 Pins on back/side (Rotation)**:
  - Pin A -> `GP8`
  - Pin B -> `GP9`
  - Center Pin (C) -> `GND`
- **2 Pins on front/side (Push Switch)**:
  - Switch Pin 1 -> `GP10`
  - Switch Pin 2 -> `GND`

---

## CircuitPython & KMK Installation

1. **Install CircuitPython**:
   - Download the latest CircuitPython `.uf2` for **RP2040-Zero**.
   - Hold the `BOOT` button on RP2040-Zero while plugging in USB.
   - Drag and drop the `.uf2` file onto the `RPI-RP2` drive.

2. **Install KMK Firmware**:
   - Download [KMK Firmware](https://github.com/KMKfw/kmk_firmware).
   - Copy the `kmk` directory into the root directory of the `CIRCUITPY` drive.

3. **Deploy Firmware Files**:
   - Copy `boot.py` and `code.py` from this repository directly onto the root of `CIRCUITPY`.

---

## Customizing Keymaps & Macros

Edit `code.py` to customize key behaviors and macros:

### Defining Custom Macros
```python
# Example Macro: Ctrl + Alt + Delete
MACRO_CAD = KC.MACRO(Press(KC.LCTRL), Press(KC.LALT), Tap(KC.DELETE), Release(KC.LALT), Release(KC.LCTRL))

# Example Macro: Typing text
MACRO_HELLO = KC.MACRO("Hello World!")
```

### Changing Keymap
Modify the 4x4 matrix in `keyboard.keymap`:
```python
keyboard.keymap = [
    # Layer 0 (Base Layer)
    [
        KC.NO,          KC.KP_SLASH, KC.KP_ASTERISK, KC.MO(1),
        KC.KP_7,        KC.KP_8,     KC.KP_9,        KC.KP_MINUS,
        KC.KP_4,        KC.KP_5,     KC.KP_6,        KC.KP_PLUS,
        KC.KP_1,        KC.KP_2,     KC.KP_3,        KC.KP_ENTER,
    ],
]
```

### Changing Rotary Encoder Controls
```python
encoder_handler.map = [
    # Layer 0: (Clockwise, Counter-Clockwise, Push Button)
    ((KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN, KC.AUDIO_MUTE),),

    # Layer 1:
    ((KC.MW_DN, KC.MW_UP, KC.MEDIA_PLAY_PAUSE),),
]
```
