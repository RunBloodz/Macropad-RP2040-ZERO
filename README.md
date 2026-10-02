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

## Arduino IDE Board Core Options

`macropad.ino` supports both popular RP2040 cores in Arduino IDE:

### Option A: Earle Philhower RP2040 Core (Recommended)
1. Open Arduino IDE -> **File** -> **Preferences**.
2. Add this URL to **Additional Boards Manager URLs**:
   ```
   https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
   ```
3. Open **Tools** -> **Board** -> **Boards Manager**, search for `rp2040` by Earle F. Philhower, and install it.
4. Select board: **Raspberry Pi Pico** or **Waveshare RP2040 Zero**.
5. Go to **Tools** -> **USB Stack** -> select **Adafruit TinyUSB**.
6. Click **Upload**.

### Option B: Arduino Mbed OS RP2040 Core
1. Open **Tools** -> **Board** -> **Arduino Mbed OS RP2040 Boards** -> select **Raspberry Pi Pico**.
2. Go to **Tools** -> **Manage Libraries...**, search for `Keyboard`, and install the standard Arduino `Keyboard` library.
3. Click **Upload**.

---

## Repository Files

* `macropad.ino` - Main Arduino IDE C++ program handling matrix scanning, key reports, and rotary encoder media keys.
* `EEPROM.h` & `EEPROM.cpp` - Lightweight RP2040 flash memory EEPROM emulation library.
* `README.md` - Board setup and compilation guide.
