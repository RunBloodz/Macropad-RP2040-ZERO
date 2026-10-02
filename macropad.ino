/*
====================================================================
 15-Key + 1 Rotary Encoder 4x4 Macropad
 Board: Waveshare RP2040-Zero / RP2040
 Environment: Arduino IDE (Adafruit TinyUSB / Earle Philhower Core)
 Features: ONLY 15 Matrix Keys + Rotary Encoder (A/B + Push Button)
====================================================================
*/

#include <Arduino.h>
#include "EEPROM.h"
#include <Adafruit_TinyUSB.h>

// ====================================================================
// HARDWARE PIN DEFINITIONS
// ====================================================================

// 4x4 Matrix Pins (COL2ROW Diodes)
const uint8_t ROW_PINS[4] = {0, 1, 2, 3};  // GP0, GP1, GP2, GP3
const uint8_t COL_PINS[4] = {4, 5, 6, 7};  // GP4, GP5, GP6, GP7

// Rotary Encoder Pins
const uint8_t ENCODER_PIN_A = 8;    // GP8
const uint8_t ENCODER_PIN_B = 9;    // GP9
const uint8_t ENCODER_PIN_BTN = 10; // GP10

// ====================================================================
// USB HID REPORT DESCRIPTOR & TINYUSB SETUP
// ====================================================================

// Keyboard + Consumer Control (Media Keys) Combined Report Descriptor
uint8_t const desc_hid_report[] = {
  TUD_HID_REPORT_DESC_KEYBOARD(HID_REPORT_ID(1)),
  TUD_HID_REPORT_DESC_CONSUMER(HID_REPORT_ID(2))
};

Adafruit_USBD_HID usb_hid;

// ====================================================================
// DEFAULT KEYMAP MATRIX (15 Keys + Encoder Slot at Row 0, Col 0)
// ====================================================================

// Map Matrix (4x4) to USB HID keycodes:
// Row 0, Col 0 is physical Encoder position, remaining 15 slots are keys
const uint8_t KEYMAP[4][4] = {
  { 0,            HID_KEY_NUM_LOCK,    HID_KEY_KEYPAD_DIVIDE,   HID_KEY_KEYPAD_MULTIPLY },
  { HID_KEY_KEYPAD_7, HID_KEY_KEYPAD_8, HID_KEY_KEYPAD_9,    HID_KEY_KEYPAD_SUBTRACT },
  { HID_KEY_KEYPAD_4, HID_KEY_KEYPAD_5, HID_KEY_KEYPAD_6,    HID_KEY_KEYPAD_ADD },
  { HID_KEY_KEYPAD_1, HID_KEY_KEYPAD_2, HID_KEY_KEYPAD_3,    HID_KEY_KEYPAD_ENTER }
};

// State variables
bool current_key_state[4][4] = {false};
bool previous_key_state[4][4] = {false};

int last_encoder_a = HIGH;
bool last_encoder_btn = HIGH;

void setup() {
  // EEPROM Initialization
  EEPROM.begin(256);

  // Initialize Matrix Row Pins (Inputs with Pull-Down for COL2ROW)
  for (int r = 0; r < 4; r++) {
    pinMode(ROW_PINS[r], INPUT_PULLDOWN);
  }

  // Initialize Matrix Column Pins (Outputs, Default LOW)
  for (int c = 0; c < 4; c++) {
    pinMode(COL_PINS[c], OUTPUT);
    digitalWrite(COL_PINS[c], LOW);
  }

  // Initialize Encoder Pins (Inputs with Internal Pull-Ups)
  pinMode(ENCODER_PIN_A, INPUT_PULLUP);
  pinMode(ENCODER_PIN_B, INPUT_PULLUP);
  pinMode(ENCODER_PIN_BTN, INPUT_PULLUP);

  // Configure TinyUSB HID
  usb_hid.setPollInterval(2);
  usb_hid.setReportDescriptor(desc_hid_report, sizeof(desc_hid_report));
  usb_hid.begin();

  // Wait for USB Device Mount
  while (!TinyUSBDevice.mounted()) {
    delay(10);
  }
}

void loop() {
  if (!usb_hid.ready()) return;

  // ------------------------------------------------------------------
  // 1. Scan 4x4 Key Matrix (15 Mechanical Switches)
  // ------------------------------------------------------------------
  uint8_t key_report[6] = {0};
  uint8_t report_count = 0;

  for (int r = 0; r < 4; r++) {
    for (int c = 0; c < 4; c++) {
      // Row 0, Col 0 is reserved for physical rotary encoder
      if (r == 0 && c == 0) continue;

      // Drive Column HIGH
      digitalWrite(COL_PINS[c], HIGH);
      delayMicroseconds(5);

      bool pressed = (digitalRead(ROW_PINS[r]) == HIGH);
      digitalWrite(COL_PINS[c], LOW);

      current_key_state[r][c] = pressed;

      if (pressed && report_count < 6) {
        key_report[report_count++] = KEYMAP[r][c];
      }
    }
  }

  // Construct standard 8-byte HID keyboard report
  // Byte 0: Modifier keys (0)
  // Byte 1: Reserved (0)
  // Bytes 2-7: Up to 6 keycodes
  hid_keyboard_report_t kb_report;
  memset(&kb_report, 0, sizeof(kb_report));
  for (uint8_t i = 0; i < report_count && i < 6; i++) {
    kb_report.keycode[i] = key_report[i];
  }

  // Send HID Keyboard Report (ID 1)
  usb_hid.sendReport(1, &kb_report, sizeof(kb_report));

  // ------------------------------------------------------------------
  // 2. Scan Rotary Encoder Rotation (Volume Control)
  // ------------------------------------------------------------------
  int current_a = digitalRead(ENCODER_PIN_A);
  if (current_a != last_encoder_a && current_a == LOW) {
    uint16_t consumer_key = 0;
    if (digitalRead(ENCODER_PIN_B) == HIGH) {
      // Rotate Right -> Volume Up
      consumer_key = HID_USAGE_CONSUMER_VOLUME_INCREMENT;
    } else {
      // Rotate Left -> Volume Down
      consumer_key = HID_USAGE_CONSUMER_VOLUME_DECREMENT;
    }
    usb_hid.sendReport16(2, consumer_key);
    delay(10);
    usb_hid.sendReport16(2, 0);
  }
  last_encoder_a = current_a;

  // ------------------------------------------------------------------
  // 3. Scan Rotary Encoder Push Button (Mute Audio)
  // ------------------------------------------------------------------
  bool current_btn = (digitalRead(ENCODER_PIN_BTN) == LOW);
  if (current_btn && !last_encoder_btn) {
    // Button Pressed -> Mute
    usb_hid.sendReport16(2, HID_USAGE_CONSUMER_MUTE);
    delay(10);
    usb_hid.sendReport16(2, 0);
  }
  last_encoder_btn = current_btn;

  delay(5);
}
