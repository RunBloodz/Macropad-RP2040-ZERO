# 15-Key + 1 Rotary Encoder Macropad (RP2040-Zero & KMK Firmware)

This repository contains the complete firmware code, USB configuration, and hardware guide for building a custom **15-Key + 1 Rotary Encoder (4x4 Matrix) Macropad** driven by Waveshare RP2040-Zero, CircuitPython, and KMK Firmware with **Vial GUI / Graphical Configurator Support**.

---

## Table of Contents
1. [Overview & Features](#overview--features)
2. [Devices & Printers & Graphical Configuration (Vial)](#devices--printers--graphical-configuration-vial)
3. [Pinout & Hardware Connections](#pinout--hardware-connections)
4. [4x4 Matrix Layout & Physical Wiring](#4x4-matrix-layout--physical-wiring)
5. [Diode Wiring & Orientation Tutorial](#diode-wiring--orientation-tutorial)
6. [Rotary Encoder Setup](#rotary-encoder-setup)
7. [Step-by-Step Soldering Tutorial](#step-by-step-soldering-tutorial)
8. [CircuitPython & KMK Installation](#circuitpython--kmk-installation)
9. [Customizing Keymaps & Macros (GUI vs Code)](#customizing-keymaps--macros-gui-vs-code)

---

## Overview & Features

- **Microcontroller**: Waveshare RP2040-Zero (RP2040 MCU with 29 GPIOs, USB-C)
- **Matrix**: 4x4 Grid (15 mechanical switches + 1 rotary encoder in top-left position `Row 0, Col 0`)
- **Rotary Encoder**: Incremental EC11 rotary encoder (Pins A/B for rotation, separate push button pin)
- **Firmware Framework**: KMK Firmware running on CircuitPython with Vial dynamic GUI engine
- **Features**:
  - Recognized by Windows/macOS/Linux under **Devices & Printers** as **"15-Key RP2040 Macropad"** by **"Custom Tech"**
  - **Graphical Key Remapping**: Configure keys, macros, layers, and rotary encoder actions visually in real-time via **Vial Web app (`https://vial.rocks`)** or standalone Vial Desktop App—no coding required!
  - Full Anti-Ghosting / NKRO with diode matrix
  - Multi-layer support (Layer 0: Numpad/Media, Layer 1: Shortcuts & Productivity Macros)
  - No backlight (maximizes power efficiency and simplifies build)

---

## Devices & Printers & Graphical Configuration (Vial)

### 1. Windows "Devices and Printers" Recognition
When you plug the macropad into Windows or macOS via USB:
- Open **Control Panel > Devices and Printers** (or **Settings > Bluetooth & Devices**).
- You will see **"15-Key RP2040 Macropad"** listed as a recognized USB HID Keyboard device.
- Right-clicking the device shows properties, device status, and manufacturer (`Custom Tech`).

```
+-------------------------------------------------------------+
|  Devices and Printers                                       |
|  +---------------------+                                    |
|  | [⌨️]                 |  Device: 15-Key RP2040 Macropad     |
|  | 15-Key RP2040       |  Manufacturer: Custom Tech          |
|  | Macropad            |  Status: Connected & Operational   |
|  +---------------------+                                    |
+-------------------------------------------------------------+
```

### 2. Graphical Customization via Web / App (Vial)
Instead of manually opening Python files to change keybindings:
1. Open your browser and navigate to **[vial.rocks](https://vial.rocks)** (or open the offline **Vial Desktop App**).
2. Click **"Connect"** and select **"15-Key RP2040 Macropad"** from the browser USB popup.
3. A visual 4x4 grid and encoder control panel will load instantly!
4. **Drag and drop keybindings, rebind encoder rotation/click, or record macros graphically in real-time.** Changes save to the macropad instantly without rebooting or reflashing.

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
   - Copy `boot.py` and `code.py` from this repository directly onto the root of `CIRCUITPY`.

---

## Customizing Keymaps & Macros (GUI vs Code)

You have two options for customizing your macropad:

### Option A: Graphical Web GUI (Vial) - Recommended
1. Open **[vial.rocks](https://vial.rocks)** in Chrome/Edge/Opera.
2. Click **Connect**, select **15-Key RP2040 Macropad**.
3. Remap keys, macros, and rotary encoder actions visually with real-time live preview.

### Option B: Code-based Customization
Directly edit `code.py` on the `CIRCUITPY` USB drive:
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
