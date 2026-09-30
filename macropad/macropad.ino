/*
====================================================================
 15-Key + 1 Rotary Encoder + Analog Axis Gamepad Controller
 Board: Waveshare RP2040-Zero
 Environment: Arduino IDE (RP2040 Earle Philhower Core / Mbed Core)
 USB Stack: Adafruit TinyUSB / USB HID
====================================================================
*/

#include <Arduino.h>
#include <EEPROM.h>
#include <Adafruit_TinyUSB.h>

// ====================================================================
// HARDWARE PIN DEFINITIONS
// ====================================================================

// 4x4 Matrix Pins
const uint8_t ROW_PINS[4] = {0, 1, 2, 3};  // GP0, GP1, GP2, GP3
const uint8_t COL_PINS[4] = {4, 5, 6, 7};  // GP4, GP5, GP6, GP7

// Rotary Encoder Pins
const uint8_t ENCODER_PIN_A = 8;    // GP8
const uint8_t ENCODER_PIN_B = 9;    // GP9
const uint8_t ENCODER_PIN_BTN = 10; // GP10

// Analog Handbrake Pin (GP26 / A0)
const uint8_t HANDBRAKE_PIN = 26;   // GP26 / A0

// ====================================================================
// CONFIGURATION & EEPROM CALIBRATION
// ====================================================================

struct Config {
  uint16_t min_v;
  uint16_t max_v;
  uint8_t dz_start;
  uint8_t dz_end;
};

Config config = {0, 1023, 0, 0};
const int EEPROM_SIZE = sizeof(Config);

void loadConfig() {
  EEPROM.begin(EEPROM_SIZE);
  uint8_t first_byte = EEPROM.read(0);
  if (first_byte != 0xFF) {
    EEPROM.get(0, config);
  }
}

void saveConfig() {
  EEPROM.put(0, config);
  EEPROM.commit();
}

// ====================================================================
// USB HID REPORT DESCRIPTOR (GAMEPAD)
// ====================================================================

uint8_t const desc_hid_report[] = {
  TUD_HID_REPORT_DESC_GAMEPAD()
};

Adafruit_USBD_HID usb_hid;

// ====================================================================
#define GAMEPAD_REPORT_ID 1

// State variables
bool matrix_state[4][4] = {false};
bool prev_matrix_state[4][4] = {false};

int last_encoder_a = HIGH;
int encoder_pos = 0;
bool last_encoder_btn = HIGH;

String serial_buffer = "";
uint16_t current_raw = 0;

// Helper functions
int processHandbrake(uint16_t raw) {
  if (config.min_v == config.max_v) return 0;

  uint16_t range_v = config.max_v - config.min_v;
  uint16_t start_v = config.min_v + (range_v * config.dz_start / 100);
  uint16_t end_v = config.max_v - (range_v * config.dz_end / 100);

  uint16_t constrained_val = constrain(raw, start_v, end_v);
  return map(constrained_val, start_v, end_v, -127, 127);
}

void setup() {
  Serial.begin(115200);

  // Initialize EEPROM
  loadConfig();

  // Initialize Matrix Pins
  for (int i = 0; i < 4; i++) {
    pinMode(ROW_PINS[i], INPUT_PULLDOWN);
    pinMode(COL_PINS[i], OUTPUT);
    digitalWrite(COL_PINS[i], LOW);
  }

  // Initialize Encoder Pins
  pinMode(ENCODER_PIN_A, INPUT_PULLUP);
  pinMode(ENCODER_PIN_B, INPUT_PULLUP);
  pinMode(ENCODER_PIN_BTN, INPUT_PULLUP);

  // Initialize USB HID
  usb_hid.setPollInterval(2);
  usb_hid.setReportDescriptor(desc_hid_report, sizeof(desc_hid_report));
  usb_hid.begin();

  while (!TinyUSBDevice.mounted()) {
    delay(10);
  }
}

void loop() {
  // 1. Read Analog Handbrake (GP26)
  uint32_t sum = 0;
  for (int i = 0; i < 8; i++) {
    sum += analogRead(HANDBRAKE_PIN);
  }
  current_raw = sum / 8;
  int8_t z_val = processHandbrake(current_raw);

  // 2. Scan Key Matrix (Row-Major: r outer, c inner)
  uint32_t buttons = 0;
  uint8_t btn_index = 1;

  for (int r = 0; r < 4; r++) {
    for (int c = 0; c < 4; c++) {
      // Drive column c HIGH
      digitalWrite(COL_PINS[c], HIGH);
      delayMicroseconds(5);

      bool pressed = (digitalRead(ROW_PINS[r]) == HIGH);

      digitalWrite(COL_PINS[c], LOW);

      // Slot (0,0) is physical Encoder position
      if (!(r == 0 && c == 0)) {
        if (pressed) {
          buttons |= (1UL << (btn_index - 1));
        }
        btn_index++;
      }
    }
  }

  // 3. Scan Rotary Encoder & Calculate Steering Axis
  int current_a = digitalRead(ENCODER_PIN_A);

  if (current_a != last_encoder_a && current_a == LOW) {
    if (digitalRead(ENCODER_PIN_B) == HIGH) {
      encoder_pos++;
    } else {
      encoder_pos--;
    }
  }
  last_encoder_a = current_a;

  int8_t joystick_x = (int8_t)constrain(encoder_pos * 10, -127, 127);

  // Encoder Push Button
  bool btn_state = digitalRead(ENCODER_PIN_BTN);
  if (btn_state == LOW) {
    buttons |= (1UL << 15); // Button 16
  }

  // 4. Send Gamepad Report via TinyUSB
  if (usb_hid.ready()) {
    hid_gamepad_report_t report = {
      .x       = joystick_x,
      .y       = 0,
      .z       = z_val,
      .rz      = 0,
      .rx      = 0,
      .ry      = 0,
      .hat     = 0,
      .buttons = buttons
    };
    usb_hid.sendReport(GAMEPAD_REPORT_ID, &report, sizeof(report));
  }

  // 5. Handle Non-blocking Serial Commands
  while (Serial.available() > 0) {
    char ch = Serial.read();
    if (ch == '\n' || ch == '\r') {
      serial_buffer.trim();
      if (serial_buffer == "READ") {
        Serial.print("RAW:");
        Serial.println(current_raw);
      } else if (serial_buffer == "PING") {
        Serial.println("PONG");
      } else if (serial_buffer == "GET_CONFIG") {
        Serial.print("CONF:");
        Serial.print(config.min_v); Serial.print(":");
        Serial.print(config.max_v); Serial.print(":");
        Serial.print(config.dz_start); Serial.print(":");
        Serial.println(config.dz_end);
      } else if (serial_buffer.startsWith("SET")) {
        int first_sp = serial_buffer.indexOf(' ');
        if (first_sp != -1) {
          String args = serial_buffer.substring(first_sp + 1);
          int v1, v2, v3, v4;
          if (sscanf(args.c_str(), "%d %d %d %d", &v1, &v2, &v3, &v4) == 4) {
            config.min_v = (uint16_t)v1;
            config.max_v = (uint16_t)v2;
            config.dz_start = (uint8_t)v3;
            config.dz_end = (uint8_t)v4;
            Serial.println("OK");
          } else {
            Serial.println("ERR");
          }
        }
      } else if (serial_buffer == "SAVE") {
        saveConfig();
        Serial.println("SAVED");
      }
      serial_buffer = "";
    } else {
      serial_buffer += ch;
      if (serial_buffer.length() > 100) serial_buffer = "";
    }
  }

  delay(5);
}
