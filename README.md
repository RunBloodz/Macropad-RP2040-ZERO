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

## Instrukcja Lutowania / Soldering Tutorial

### 1. Diodes Orientation (COL2ROW) / Orientacja Diod
* Every mechanical switch needs a 1N4148 diode in series to prevent ghosting.
* **Orientation**: Solder diode with the **black line / cathode side** pointing towards the **Row pin (GP0–GP3)**.
* The anode side connects to one leg of the mechanical switch. The other leg of the switch connects to the **Column pin (GP4–GP7)**.

### 2. Matrix Wiring Steps / Krok po Kroku
1. **Columns Wiring**: Connect one side of all switches in Column 0 to `GP4`, Column 1 to `GP5`, Column 2 to `GP6`, Column 3 to `GP7`.
2. **Rows Wiring**: Connect the cathode (black band side) of the diodes in Row 0 to `GP0`, Row 1 to `GP1`, Row 2 to `GP2`, Row 3 to `GP3`.
3. **Rotary Encoder Wiring**:
   - Solder Encoder Pin A to **GP8**.
   - Solder Encoder Pin B to **GP9**.
   - Solder Encoder Common / Ground pin to **GND**.
   - Solder Encoder Switch Pin to **GP10** (other side to **GND**).

---

## Rozwiązanie Błędu Kompilacji w Arduino IDE / Resolving Compilation Errors

### Przyczyna błędu `Adafruit_USBH_CDC.h: error: expected class-name before '{' token`
Ten błąd występuje, gdy w Arduino IDE wybrana jest płytka **Arduino Mbed OS RP2040**, a jednocześnie zainstalowana jest globalna biblioteka **Adafruit TinyUSB Library**. Biblioteka `Adafruit_TinyUSB_Library` jest przeznaczona dla rdzenia **Earle Philhower RP2040 Core**.

### Jak to naprawić / How to fix:
1. W Arduino IDE wybierz **Plik** -> **Preferencje** (**File** -> **Preferences**).
2. Dodaj poniższy URL do **Dodatkowe adresy URL do menedżera płytek**:
   ```
   https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json
   ```
3. Otwórz **Narzędzia** -> **Płytka** -> **Menedżer płytek**, wyszukaj `rp2040` (autor: Earle F. Philhower) i zainstaluj go.
4. Wybierz płytkę: **Raspberry Pi Pico** lub **Waveshare RP2040 Zero** pod sekcją `Raspberry Pi RP2040 Boards`.
5. Przejdź do **Narzędzia** -> **USB Stack** -> wybierz **Adafruit TinyUSB**.
6. Kliknij **Wgraj** (Upload).

---

## Pliki w repozytorium / Repository Files

* `macropad.ino` - Główny program C++ w Arduino IDE do obsługi macierzy i enkodera.
* `EEPROM.h` & `EEPROM.cpp` - Lekka biblioteka emulacji EEPROM w pamięci Flash RP2040.
* `HID.h` - Nagłówek pomocniczy zapewniający definicje klawiszy.
* `README.md` - Instrukcja lutowania, konfiguracji i podłączenia.
