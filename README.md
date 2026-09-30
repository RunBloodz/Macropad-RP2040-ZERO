# 15-Key + 1 Rotary Encoder Macropad (RP2040-Zero & KMK Firmware)

This repository contains the complete firmware code, USB configuration, and hardware guide for building a custom **15-Key + 1 Rotary Encoder (4x4 Matrix) Macropad** driven by Waveshare RP2040-Zero, CircuitPython, and KMK Firmware with **pip installation, Pipkin support, & deployment tools**.

---

## Table of Contents
1. [Quick Start (pip install & pipkin)](#quick-start-pip-install--pipkin)
2. [Overview & Features](#overview--features)
3. [Device Manager & Hardware Identification](#device-manager--hardware-identification)
4. [Configuring Keys via Windows Device Manager & Software](#configuring-keys-via-windows-device-manager--software)
5. [Pinout & Hardware Connections](#pinout--hardware-connections)
6. [4x4 Matrix Layout & Physical Wiring](#4x4-matrix-layout--physical-wiring)
7. [Diode Wiring & Orientation Tutorial](#diode-wiring--orientation-tutorial)
8. [Rotary Encoder Setup](#rotary-encoder-setup)
9. [Step-by-Step Soldering Tutorial](#step-by-step-soldering-tutorial)
10. [CircuitPython & KMK Installation](#circuitpython--kmk-installation)
11. [Customizing Keymaps & Macros](#customizing-keymaps--macros)

---

## Quick Start (pip install & pipkin)

### Option 1: Standard pip & `macropad-deploy`
You can install this project directly via `pip` and use the built-in `macropad-deploy` CLI command to automatically find your connected RP2040-Zero board (`CIRCUITPY` drive) and copy `code.py` and `boot.py`:

```bash
# Clone the repository
git clone https://github.com/example/rp2040-macropad.git
cd rp2040-macropad

# Install package via pip
pip install .

# Automatically deploy firmware files to connected CIRCUITPY drive
macropad-deploy
```

### Option 2: Installing CircuitPython Libraries via Pipkin
If you use **Pipkin** (the CircuitPython package manager) to manage libraries directly on your target RP2040 board:

```bash
# Install dependencies directly to connected CIRCUITPY drive using pipkin
pipkin install -r requirements-pipkin.txt
```

---

## Overview & Features

- **Microcontroller**: Waveshare RP2040-Zero (RP2040 MCU with 29 GPIOs, USB-C)
- **Matrix**: 4x4 Grid (15 mechanical switches + 1 rotary encoder in top-left position `Row 0, Col 0`)
- **Rotary Encoder**: Incremental EC11 rotary encoder (Pins A/B for rotation, separate push button pin)
- **Firmware Framework**: KMK Firmware running on CircuitPython with Vial dynamic GUI engine
- **Features**:
  - Recognized natively in **Windows Device Manager** as **"15-Key RP2040 Macropad"** under Keyboards and Human Interface Devices
  - **3 Flexible Configuration Methods**:
    1. **Direct Web/App GUI (Vial / `https://vial.rocks`)**: Plug in and rebind keys instantly without reflashing
    2. **Windows Device Manager + PowerToys Keyboard Manager**: Customize key behavior per-device natively in Windows
    3. **On-board Python Script (`code.py`)**: Directly edit python code on the USB drive
  - Full Anti-Ghosting / NKRO with diode matrix
  - Multi-layer support (Layer 0: Numpad/Media, Layer 1: Shortcuts & Productivity Macros)
  - No backlight (maximizes power efficiency and simplifies build)

---

## Device Manager & Hardware Identification

When connected via USB, `boot.py` supplies custom USB HID descriptors so Windows Device Manager registers the device with its full name and manufacturer details:

1. Press `Win + X` and select **Device Manager** (or type `devmgmt.msc` in Run).
2. Expand **Keyboards** and **Human Interface Devices (HID)**.
3. You will see **"15-Key RP2040 Macropad"** listed under connected devices with Manufacturer **"Custom Tech"**.

```
[Device Manager]
 ├── ⌨️ Keyboards
 │    └── ⌨️ 15-Key RP2040 Macropad (Custom Tech)
 └── 🎮 Human Interface Devices
      └── 🔌 HID-compliant consumer control device
```

---

## Configuring Keys via Windows Device Manager & Software

To configure and remap key functions for your macropad on Windows, you have three powerful options:

### Method 1: Windows PowerToys (Device-Specific Native Windows Remapping)
Microsoft provides **Microsoft PowerToys Keyboard Manager**, which directly interfaces with HID keyboard devices detected in Device Manager:
1. Install **Microsoft PowerToys** (available from Microsoft Store or GitHub).
2. Open **PowerToys > Keyboard Manager**.
3. Click **Remap a key** or **Remap a shortcut**.
4. Press any key on your **15-Key RP2040 Macropad**—PowerToys will detect the keypress from the macropad and allow you to reassign it to any key, media action, shortcut, or application launch in Windows!

### Method 2: Real-time Web GUI Remapping (Vial / WebUSB)
You can configure keybindings and macros directly on the hardware in real-time:
1. Open Chrome/Edge/Opera and go to **[vial.rocks](https://vial.rocks)** (or use the Vial Desktop App).
2. Click **Connect** and select **15-Key RP2040 Macropad**.
3. Drag and drop keys, rebind rotary encoder turns/clicks, or create macros graphically. Changes save directly to the macropad memory instantly!

### Method 3: AutoHotkey (AHK Scripting)
For complex automation on Windows, target keypresses sent by the macropad using AutoHotkey scripts:
```autohotkey
; AutoHotkey script for 15-Key Macropad
Numpad1::
Run, notepad.exe
return
```

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
Change line in `code.py`:
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

## Step-by-Step Soldering Tutorial

### Required Tools & Materials
1. **Soldering Iron** (Temperature set to ~320°C–350°C / 600°F–660°F)
2. **Solder Wire** (60/40 rosin-core or lead-free solder wire)
3. **Flux Pen** or Paste (helps solder flow cleanly)
4. **Flush Cutters** (to clip diode legs)
5. **Solid Core or Stranded Wires** (28-30 AWG)
6. **15x Mechanical Switches** (MX-style) & **1x EC11 Rotary Encoder**
7. **15x 1N4148 Diodes**
8. **Waveshare RP2040-Zero Board**

---

### Step 1: Prepare and Solder the Diodes to the Switches
1. Take a **1N4148 diode**. Bend the **Anode leg** (plain side without stripe) around Pin 1 of a mechanical switch.
2. Ensure the **Cathode leg** (side with the **black stripe**) points outwards away from the switch.
3. Apply a small touch of flux, touch the soldering iron tip to the joint for 2 seconds, and apply solder.
4. Trim excess lead wire on the Anode side using flush cutters.
5. Repeat for all **15 mechanical switches**.

---

### Step 2: Solder the Matrix Rows
1. Align the 15 switches in your plate/case grid (positions `(R0,C1)` through `(R3,C3)`).
2. Bend the Cathode legs (black stripe side) of all diodes in **Row 0** towards each other so they touch in a continuous line.
3. Solder the diode Cathodes together across each row:
   - **Row 0**: Connect diode cathodes of keys `(0,1)`, `(0,2)`, `(0,3)`.
   - **Row 1**: Connect diode cathodes of keys `(1,0)`, `(1,1)`, `(1,2)`, `(1,3)`.
   - **Row 2**: Connect diode cathodes of keys `(2,0)`, `(2,1)`, `(2,2)`, `(2,3)`.
   - **Row 3**: Connect diode cathodes of keys `(3,0)`, `(3,1)`, `(3,2)`, `(3,3)`.
4. Clip off the excess diode legs after soldering each row wire.

---

### Step 3: Solder the Matrix Columns
1. Take insulated wire (e.g. 28 AWG) and strip small windows corresponding to each column position.
2. Solder the wire directly to **Pin 2** (the non-diode pin) of all switches in the same column:
   - **Column 0 Wire**: Connects Pin 2 of keys `(1,0)`, `(2,0)`, `(3,0)`.
   - **Column 1 Wire**: Connects Pin 2 of keys `(0,1)`, `(1,1)`, `(2,1)`, `(3,1)`.
   - **Column 2 Wire**: Connects Pin 2 of keys `(0,2)`, `(1,2)`, `(2,2)`, `(3,2)`.
   - **Column 3 Wire**: Connects Pin 2 of keys `(0,3)`, `(1,3)`, `(2,3)`, `(3,3)`.

---

### Step 4: Solder the Rotary Encoder
The rotary encoder sits in slot **(Row 0, Column 0)**.
1. Place the **EC11 Rotary Encoder** into the top-left slot.
2. **Rotation Pins (3 pins side)**:
   - Solder a wire from **Pin A** to RP2040-Zero **GP8**.
   - Solder a wire from **Center Pin (C)** to RP2040-Zero **GND**.
   - Solder a wire from **Pin B** to RP2040-Zero **GP9**.
3. **Push Switch Pins (2 pins side)**:
   - Solder a wire from **Switch Pin 1** to RP2040-Zero **GP10**.
   - Solder a wire from **Switch Pin 2** to RP2040-Zero **GND** (you can bridge this to Center Pin C on GND).

---

### Step 5: Connect Matrix Rows & Columns to RP2040-Zero
Solder lead wires from each row and column bus to the RP2040-Zero pins:

| Matrix Line | RP2040-Zero Pin | Solder Point Description |
| :--- | :--- | :--- |
| **Row 0** | `GP0` | Wire from Row 0 diode bus to RP2040-Zero `GP0` pad |
| **Row 1** | `GP1` | Wire from Row 1 diode bus to RP2040-Zero `GP1` pad |
| **Row 2** | `GP2` | Wire from Row 2 diode bus to RP2040-Zero `GP2` pad |
| **Row 3** | `GP3` | Wire from Row 3 diode bus to RP2040-Zero `GP3` pad |
| **Col 0** | `GP4` | Wire from Column 0 wire bus to RP2040-Zero `GP4` pad |
| **Col 1** | `GP5` | Wire from Column 1 wire bus to RP2040-Zero `GP5` pad |
| **Col 2** | `GP6` | Wire from Column 2 wire bus to RP2040-Zero `GP6` pad |
| **Col 3** | `GP7` | Wire from Column 3 wire bus to RP2040-Zero `GP7` pad |

---

### Step 6: Visual Inspection & Continuity Check
1. **Check for Shorts**: Inspect all joints with a magnifying glass or multimeter continuity mode. Ensure no adjacent wires or RP2040-Zero pads touch each other.
2. **Diode Check**: Confirm that all diode black stripes face towards the row wires.
3. **GND Check**: Verify that encoder center pin and push switch share a clean connection to `GND`.

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
   - Run `macropad-deploy` from your terminal or copy `boot.py` and `code.py` directly onto `CIRCUITPY`.

---

## Customizing Keymaps & Macros

You have three convenient ways to customize your macropad keymaps:

### Option A: Web GUI (Vial / `vial.rocks`)
- Open **[vial.rocks](https://vial.rocks)** in your web browser.
- Select **15-Key RP2040 Macropad** and dynamically assign keys and macros via drag-and-drop.

### Option B: Windows PowerToys Keyboard Manager
- Open **PowerToys > Keyboard Manager**.
- Select the **15-Key RP2040 Macropad** key to remap to any shortcut, key, or program.

### Option C: Python Code Customization
Directly edit `code.py` on the `CIRCUITPY` drive:
```python
# Custom Hotkey Combination
MACRO_TASK_MGR = KC.MACRO(Press(KC.LCTRL), Press(KC.LSHIFT), Tap(KC.ESCAPE), Release(KC.LSHIFT), Release(KC.LCTRL))

# Custom Keymap Grid
keyboard.keymap = [
    [
        KC.NO,          KC.KP_SLASH,    KC.KP_ASTERISK, KC.MO(1),
        KC.KP_7,        KC.KP_8,        KC.KP_9,        KC.KP_MINUS,
        KC.KP_4,        KC.KP_5,        KC.KP_6,        KC.KP_PLUS,
        KC.KP_1,        KC.KP_2,        KC.KP_3,        KC.KP_ENTER,
    ],
]
```
