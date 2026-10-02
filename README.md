# 15-Key + 1 Rotary Encoder RP2040 Macropad

A lightweight, high-performance 15-key mechanical switch + 1 rotary encoder USB HID macropad program written in C++ for the RP2040 (Waveshare RP2040-Zero, Raspberry Pi Pico, etc.).

---

## Hardware Features & Pinout

* **MCU**: Waveshare RP2040-Zero (or any RP2040 board)
* **Matrix**: 4x4 grid (15 mechanical switches + 1 rotary encoder position at Row 0, Col 0)
* **Diodes**: `COL2ROW` orientation (Cathode/band pointing to Row pins GP0–GP3)

| Component | Function | Pins |
| :--- | :--- | :--- |
| **Matrix Rows (4)** | Row 0, 1, 2, 3 | `GP0`, `GP1`, `GP2`, `GP3` |
| **Matrix Cols (4)** | Col 0, 1, 2, 3 | `GP4`, `GP5`, `GP6`, `GP7` |
| **Rotary Encoder Pin A** | Encoder Phase A | `GP8` |
| **Rotary Encoder Pin B** | Encoder Phase B | `GP9` |
| **Rotary Encoder Button** | Dedicated Switch Pin (Click) | `GP10` |

---

## How to Resolve `HID.h: No such file or directory` in Arduino IDE

If you encountered `fatal error: HID.h: No such file or directory` when compiling in Arduino IDE:

### Cause
The standard AVR `Keyboard` library was installed globally in your Arduino libraries folder. The AVR `Keyboard` library requires `HID.h` (an AVR-specific core header) and is not compatible with RP2040.

### Solution
1. Open Arduino IDE -> **Tools** -> **Board** -> Select **Raspberry Pi Pico** or **Waveshare RP2040 Zero** (under Earle Philhower RP2040 Core).
2. Go to **Tools** -> **USB Stack** -> select **Adafruit TinyUSB**.
3. Compile and Upload. The provided code automatically uses `Adafruit_TinyUSB.h` built into the RP2040 core.

---

## Repository Files

* `macropad.ino` - Main Arduino IDE C++ program handling matrix scanning, key reports, and rotary encoder media keys.
* `EEPROM.h` & `EEPROM.cpp` - Lightweight RP2040 flash memory EEPROM emulation library.
* `HID.h` - Stub header providing macro definitions for RP2040 compatibility.
* `README.md` - Board setup and compilation guide.
