# 15-Key + 1 Rotary Encoder + Analog Axis Gamepad (RP2040-Zero)

This repository contains the complete firmware code (CircuitPython & Arduino C++ `.ino`), USB configuration, persistent EEPROM/NVM calibration, and hardware guide for building a custom **15-Key + 1 Rotary Encoder + 1 Analog Axis (Handbrake / Potentiometer) USB Gamepad Controller** driven by Waveshare RP2040-Zero.

---

## Table of Contents
1. [Arduino IDE Installation & Setup (.ino)](#arduino-ide-installation--setup-ino)
2. [Quick Start (pip install & CircuitPython)](#quick-start-pip-install--circuitpython)
3. [Overview & Features](#overview--features)
4. [Serial Control Protocol & Calibration Commands](#serial-control-protocol--calibration-commands)
5. [Gamepad Testing in Windows (`joy.cpl`) & Device Manager](#gamepad-testing-in-windows-joycpl--device-manager)
6. [Gamepad Layout & Button Assignment](#gamepad-layout--button-assignment)
7. [Pinout & Hardware Connections](#pinout--hardware-connections)
8. [4x4 Matrix Layout & Physical Wiring](#4x4-matrix-layout--physical-wiring)
9. [Diode Wiring & Orientation Tutorial](#diode-wiring--orientation-tutorial)
10. [Rotary Encoder & Analog Axis Setup](#rotary-encoder--analog-axis-setup)
11. [Step-by-Step Soldering Tutorial](#step-by-step-soldering-tutorial)

---

## Arduino IDE Installation & Setup (.ino)

If you prefer programming the RP2040-Zero in **C++ / Arduino IDE**:

1. **Install Board Package**:
   - In Arduino IDE, go to **Tools > Board > Boards Manager...**
   - Search for **Raspberry Pi Pico/RP2040 by Earle F. Philhower** and install it.
2. **Open Sketch**:
   - Open `macropad/macropad.ino` in Arduino IDE.
3. **Configure Board Settings**:
   - **Board**: `Raspberry Pi Pico` or `Waveshare RP2040-Zero`
   - **USB Stack**: `Adafruit TinyUSB`
4. **Compile & Upload**:
   - Put RP2040-Zero into bootloader mode (hold `BOOT` while plugging in USB).
   - Click **Upload** in Arduino IDE.

---

## Quick Start (pip install & CircuitPython)

### Option 1: Standard pip & `macropad-deploy`
```bash
git clone https://github.com/example/rp2040-macropad.git
cd rp2040-macropad
pip install .
macropad-deploy
```

### Option 2: Installing CircuitPython Libraries via Pipkin
```bash
pipkin install -r requirements-pipkin.txt
```

---

## Overview & Features

- **Microcontroller**: Waveshare RP2040-Zero (RP2040 MCU with 29 GPIOs, USB-C)
- **Matrix**: 4x4 Grid (15 mechanical switches + 1 rotary encoder in top-left position `Row 0, Col 0`)
- **Analog Axis**: Potentiometer / Handbrake input on **GP26 (ADC0)** with EEPROM/NVM persistent calibration and deadzone processing
- **Rotary Encoder**: Incremental EC11 rotary encoder (Pins A/B for rotation mapped to Joystick X-Axis Steering, push button mapped to Gamepad Button 16)
- **Firmware Support**: Both **Arduino C++ (`macropad/macropad.ino`)** and **CircuitPython (`code.py`)**
- **Serial Calibration Protocol**: Non-blocking serial protocol over USB CDC for real-time calibration (`PING`, `READ`, `GET_CONFIG`, `SET`, `SAVE`)

---

## Serial Control Protocol & Calibration Commands

The macropad provides a non-blocking serial communication interface via USB Serial (CDC) to calibrate the analog handbrake / potentiometer on **GP26**:

| Command | Response Example | Description |
| :--- | :--- | :--- |
| `PING` | `PONG` | Verifies serial connection |
| `READ` | `RAW:32768` | Reads current raw ADC potentiometer value |
| `GET_CONFIG` | `CONF:0:1023:0:0` | Returns current calibration parameters (`min:max:deadzone_start:deadzone_end`) |
| `SET <min> <max> <dz_start> <dz_end>` | `OK` or `SET_ERR` | Updates runtime calibration settings in memory |
| `SAVE` | `SAVED` | Flashes calibration values into non-volatile EEPROM/flash memory |

---

## Gamepad Testing in Windows (`joy.cpl`) & Device Manager

1. Press `Win + R`, type `joy.cpl`, and press **Enter**.
2. Select **15-Key RP2040 Gamepad Controller** and click **Properties**:
   - Pressing keys lights up **Buttons 1 through 15**.
   - Turning the **Rotary Encoder** adjusts the **X-Axis Joystick indicator** (Steering).
   - Pulling the **Handbrake/Potentiometer (GP26)** moves the **Z-Axis**.
   - Pressing the **Rotary Encoder Push Knob** triggers **Button 16**.

---

## Gamepad Layout & Button Assignment

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
| **Analog Handbrake**| Signal Input | `GP26` | Potentiometer / Hall Sensor (ADC0) |
| **Power / Ground**| 3.3V & GND | `3V3` / `GND` | Power for Potentiometer / Encoder |

---

## Diode Wiring & Orientation Tutorial

### Diode Polarization
- **Anode (+)**: Plain body side connected to Column line.
- **Cathode (-)**: Black stripe side connected to Row line (`COL2ROW`).

---

## Step-by-Step Soldering Tutorial

1. **Diodes to Switches**: Solder diode Anodes to Pin 1 of each switch.
2. **Row Bus**: Solder diode Cathodes together across each row (`GP0..GP3`).
3. **Column Bus**: Solder Pin 2 down each column (`GP4..GP7`).
4. **Rotary Encoder**: Connect Pins A/B to `GP8` & `GP9`, Switch to `GP10`, Center pin to `GND`.
5. **Analog Handbrake (GP26)**: Connect potentiometer outer pins to `3V3` and `GND`, and wiper wiper signal to `GP26`.
