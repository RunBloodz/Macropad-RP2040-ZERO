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

## Windows Key Editing via Serial CDC / Edycja Klawiszy w Windows

You can edit key assignments dynamically in Windows using **Arduino Serial Monitor**, **PuTTY**, **Tera Term**, or any serial terminal over the device's COM port (115200 baud).

### Serial Commands / Komendy Serial
* `GET` - Displays current 4x4 matrix keymap in HEX format.
* `SET <row> <col> <hex_keycode>` - Changes keycode at matrix position (Row 0..3, Col 0..3).
  * *Example*: `SET 0 1 04` sets Row 0, Col 1 to Key 'A' (`0x04`).
* `SAVE` - Saves current active keymap into EEPROM flash memory.
* `RESET` - Restores default keypad keymap.
* `HELP` - Displays command usage help.

### Common USB HID Keycodes (HEX)
| Key | HEX Code | Key | HEX Code |
| :--- | :--- | :--- | :--- |
| **A – Z** | `0x04` – `0x1D` | **Keypad 1 – 9** | `0x59` – `0x61` |
| **1 – 0** | `0x1E` – `0x27` | **Num Lock** | `0x53` |
| **ENTER** | `0x28` | **Keypad / (Divide)** | `0x54` |
| **ESCAPE** | `0x29` | **Keypad * (Multiply)** | `0x55` |
| **BACKSPACE**| `0x2A` | **Keypad - (Subtract)** | `0x56` |
| **TAB** | `0x2B` | **Keypad + (Add)** | `0x57` |
| **SPACE** | `0x2C` | **Keypad ENTER** | `0x58` |

---

## Warunki Konfiguracji Arduino IDE / How to Fix Compilation Error

### Przyczyna błędu `Adafruit_USBH_CDC.h: error: expected class-name before '{' token`
Ten błąd pojawia się, gdy w Arduino IDE wybrana jest płytka **Arduino Mbed OS RP2040** (`mbed_rp2040`), która nie wspiera bezpośrednio biblioteki Adafruit TinyUSB.

### Instrukcja krok po kroku (Krok po kroku w Arduino IDE):

1. Otwórz Arduino IDE -> **Plik** -> **Preferencje** (**File** -> **Preferences**).
2. Wklej poniższy adres URL do pola **Dodatkowe adresy URL do menedżera płytek** (**Additional Boards Manager URLs**):
   ```text
   https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
   ```
3. Przejdź do **Narzędzia** -> **Płytka** -> **Menedżer płytek** (**Tools** -> **Board** -> **Boards Manager**).
4. Wyszukaj `rp2040` i zainstaluj paczkę **Raspberry Pi Pico/RP2040** autorstwa **Earle F. Philhower, III**.
5. W menu **Narzędzia** -> **Płytka** (**Tools** -> **Board**) wybierz:
   - **Raspberry Pi RP2040 Boards** -> **Waveshare RP2040 Zero** (lub **Raspberry Pi Pico**).
6. W menu **Narzędzia** -> **USB Stack** (**Tools** -> **USB Stack**) wybierz **Adafruit TinyUSB**.
7. Kliknij **Wgraj** (**Upload**).

---

## Instrukcja Lutowania / Soldering Tutorial

### 1. Diodes Orientation (COL2ROW) / Orientacja Diod
* Każdy przełącznik mechaniczny wymaga diody 1N4148 zapobiegającej "ghostingowi".
* **Orientacja**: Przylutuj diodę z **czarnym paskiem (katodą)** skierowanym w stronę **pinu wiersza (GP0–GP3)**.
* Anoda diody łączy się z jedną nóżką przełącznika, a druga nóżka przełącznika łączy się z **pinem kolumny (GP4–GP7)**.

### 2. Schemat Połączeń Enkodera / Encoder Wiring
* Enkoder A -> **GP8**
* Enkoder B -> **GP9**
* Przycisk Enkodera -> **GP10**
* Mass / Masa -> **GND**

---

## Pliki w repozytorium / Repository Files

* `macropad.ino` - Główny program C++ w Arduino IDE z obsługą USB CDC key-editing, macierzy i enkodera.
* `EEPROM.h` & `EEPROM.cpp` - Lekka biblioteka emulacji EEPROM w pamięci Flash RP2040.
* `HID.h` - Nagłówek pomocniczy zapewniający definicje klawiszy.
* `README.md` - Instrukcja lutowania, konfiguracji i podłączenia.
