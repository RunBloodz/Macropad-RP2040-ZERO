# 15-Key + 1 Rotary Encoder USB Gamepad Controller (RP2040-Zero)

This repository contains the complete firmware code, USB configuration, and hardware guide for building a custom **15-Key + 1 Rotary Encoder (4x4 Matrix) USB Gamepad / Macro Controller** driven by Waveshare RP2040-Zero and CircuitPython.

---

## Table of Contents
1. [Quick Start (pip install & pipkin)](#quick-start-pip-install--pipkin)
2. [Overview & Features](#overview--features)
3. [Gamepad Testing in Windows (`joy.cpl`) & Device Manager](#gamepad-testing-in-windows-joycpl--device-manager)
4. [Gamepad Layout & Button Assignment](#gamepad-layout--button-assignment)
5. [Pinout & Hardware Connections](#pinout--hardware-connections)
6. [4x4 Matrix Layout & Physical Wiring](#4x4-matrix-layout--physical-wiring)
7. [Diode Wiring & Orientation Tutorial](#diode-wiring--orientation-tutorial)
8. [Rotary Encoder Setup](#rotary-encoder-setup)
9. [Step-by-Step Soldering Tutorial](#step-by-step-soldering-tutorial)
10. [CircuitPython Installation](#circuitpython-installation)
11. [Customizing Gamepad Mapping & Profiles](#customizing-gamepad-mapping--profiles)

---

## Quick Start (pip install & pipkin)

### Option 1: Standard pip & `macropad-deploy`
Install this project directly via `pip` and use the built-in `macropad-deploy` CLI command to automatically find your connected RP2040-Zero board (`CIRCUITPY` drive) and copy `code.py` and `boot.py`:

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
- **Rotary Encoder**: Incremental EC11 rotary encoder (Pins A/B for rotation mapped to Joystick X-Axis Steering/Throttle, separate push button pin mapped to Gamepad Button 16)
- **USB HID Protocols**: Native Gamepad (`usb_hid.Device.GAMEPAD`), Keyboard, Consumer Control, Mouse
- **Features**:
  - Recognized natively in Windows/Linux/macOS as **"15-Key RP2040 Gamepad Controller"**
  - **Windows Game Controllers Utility (`joy.cpl`)**: Test all 16 buttons and joystick axes natively in Windows
  - Hardware-level anti-ghosting with diode matrix (`COL2ROW`)
  - Multi-profile support (Profile 0: Standard Gamepad Buttons 1..16 + Steering Axis, Profile 1: Flight / Sim Racing / Keyboard Hotkeys)
  - No backlight (maximizes power efficiency and simplifies build)

---

## Gamepad Testing in Windows (`joy.cpl`) & Device Manager

When connected via USB, `boot.py` configures standard Gamepad HID descriptors so Windows recognizes the board as a full Game Controller:

1. Press `Win + R`, type `joy.cpl`, and press **Enter**.
2. You will see **"15-Key RP2040 Gamepad Controller"** listed in the Game Controllers window.
3. Click **Properties** to open the live test window:
   - Pressing any key lights up **Buttons 1 through 15**.
   - Turning the **Rotary Encoder** moves the **X-Axis Joystick indicator** smoothly back and forth (perfect for steering or throttle).
   - Pressing the **Rotary Encoder Push Knob** triggers **Button 16**.

```
[Windows Game Controllers - joy.cpl]
 ├── Installed Game Controllers:
 │    └── 🎮 15-Key RP2040 Gamepad Controller (Status: OK)
 └── [Properties Window]
      ├── Buttons: [1] [2] [3] [4] [5] [6] [7] [8] ... [16]
      └── Axes:    X-Axis (Steering / Encoder Knob)
```

---

## Gamepad Layout & Button Assignment

The 4x4 matrix layout corresponds to 16 physical grid positions. Position `(Row 0, Col 0)` holds the Rotary Encoder knob.

```
+-------------------+-------------------+-------------------+-------------------+
|  [ENCODER KNOB]   |  [KEY 1] (R0,C1)  |  [KEY 2] (R0,C2)  |  [KEY 3] (R0,C3)  |
|  X-Axis Steering  |  Gamepad Btn 1    |  Gamepad Btn 2    |  Profile 1 Hold   |
|  Press: Btn 16    |  (e.g. Cross/A)   |  (e.g. Circle/B)  |                   |
+-------------------+-------------------+-------------------+-------------------+
|  [KEY 4] (R1,C0)  |  [KEY 5] (R1,C1)  |  [KEY 6] (R1,C2)  |  [KEY 7] (R1,C3)  |
|  Gamepad Btn 3    |  Gamepad Btn 4    |  Gamepad Btn 5    |  Gamepad Btn 6    |
|  (e.g. Square/X)  |  (e.g. Triangle/Y)|  (e.g. L1/LB)     |  (e.g. R1/RB)     |
+-------------------+-------------------+-------------------+-------------------+
|  [KEY 8] (R2,C0)  |  [KEY 9] (R2,C1)  |  [KEY 10] (R2,C2) |  [KEY 11] (R2,C3) |
|  Gamepad Btn 7    |  Gamepad Btn 8    |  Gamepad Btn 9    |  Gamepad Btn 10   |
|  (e.g. L2/LT)     |  (e.g. R2/RT)     |  (Select/Back)    |  (Start)          |
+-------------------+-------------------+-------------------+-------------------+
|  [KEY 12] (R3,C0) |  [KEY 13] (R3,C1) |  [KEY 14] (R3,C2) |  [KEY 15] (R3,C3) |
|  Gamepad Btn 11   |  Gamepad Btn 12   |  Gamepad Btn 13   |  Gamepad Btn 14   |
|  (L3)             |  (R3)             |  (Home)           |  (Custom)         |
+-------------------+-------------------+-------------------+-------------------+
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
| **Rotary Encoder**| Channel A | `GP8` | Rotation pin A (X-Axis) |
| | Channel B | `GP9` | Rotation pin B (X-Axis) |
| | Switch (Button)| `GP10` | Gamepad Button 16 (GND on other side) |
| | Common / GND | `GND` | Ground pin for Encoder |

---

## Diode Wiring & Orientation Tutorial

### Why Use Diodes?
Diodes prevent "ghosting" or "masking" when holding multiple buttons simultaneously. Recommended diodes: **1N4148** signal diodes (axial or SMD).

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

Our firmware defaults to `columns_to_anodes=True` (equivalent to `COL2ROW`).

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

---

## Step-by-Step Soldering Tutorial

### Required Tools & Materials
1. **Soldering Iron** (Temperature set to ~320°C–350°C)
2. **Solder Wire** (60/40 rosin-core or lead-free solder wire)
3. **Flux Pen** or Paste
4. **Flush Cutters** (to clip diode legs)
5. **Solid Core or Stranded Wires** (28-30 AWG)
6. **15x Mechanical Switches** & **1x EC11 Rotary Encoder**
7. **15x 1N4148 Diodes**
8. **Waveshare RP2040-Zero Board**

---

### Step 1: Prepare and Solder the Diodes to the Switches
1. Take a **1N4148 diode**. Bend the **Anode leg** (plain side without stripe) around Pin 1 of a mechanical switch.
2. Ensure the **Cathode leg** (side with the **black stripe**) points outwards away from the switch.
3. Apply a small touch of flux and solder the joint. Repeat for all **15 mechanical switches**.

### Step 2: Solder Matrix Rows
1. Connect diode Cathodes together across each row (Row 0, Row 1, Row 2, Row 3).

### Step 3: Solder Matrix Columns
1. Connect Pin 2 of all switches down each column (Col 0, Col 1, Col 2, Col 3).

### Step 4: Connect to RP2040-Zero
1. Solder Row lines to `GP0..GP3`.
2. Solder Column lines to `GP4..GP7`.
3. Solder Encoder Pins A & B to `GP8` & `GP9`, Encoder Push Switch to `GP10`, and Common/Center pin to `GND`.

---

## CircuitPython Installation

1. **Install CircuitPython**:
   - Download the latest CircuitPython `.uf2` for **RP2040-Zero**.
   - Hold `BOOT` button while plugging in USB, then drag and drop the `.uf2` file onto `RPI-RP2`.

2. **Deploy Firmware Files**:
   - Run `macropad-deploy` from your terminal or copy `boot.py` and `code.py` directly onto `CIRCUITPY`.
   - Copy the `adafruit_hid` library folder onto the `CIRCUITPY/lib/` drive.

---

## Customizing Gamepad Mapping & Profiles

Edit `code.py` on your `CIRCUITPY` drive to customize button bindings and profiles:

```python
KEYMAP = {
    # Profile 0: Gamepad Buttons
    0: [
        ('NONE', None),         # Slot 0 (Encoder Knob)
        ('GAMEPAD', 1),         # Button 1
        ('GAMEPAD', 2),         # Button 2
        ('LAYER_HOLD', 1),      # Hold to switch to Profile 1
        ('GAMEPAD', 3),         # Button 3
        # ...
    ],
}
```
