/*
====================================================================
 15-Key + 1 Rotary Encoder 4x4 Macropad
 Board: Waveshare RP2040-Zero / RP2040 MCU
 Hardware: 15 Mechanical Keys + 1 EC11 Rotary Encoder (A, B, Push Button)
 Diodes: COL2ROW orientation

 Rotary Encoder Pin Mapping:
   - GP8 : Phase A
   - GP9 : Phase B
   - GP10: Click Push Button

 Board Core Compatibility:
   - Earle Philhower RP2040 Core (Tools -> USB Stack -> Adafruit TinyUSB)
   - Arduino Mbed OS RP2040 Core (Standard Keyboard library)
====================================================================
*/

#include <Arduino.h>
#include "EEPROM.h"

// HID Keycodes definitions
#ifndef HID_KEY_NUM_LOCK
#define HID_KEY_NUM_LOCK          0x53
#define HID_KEY_KEYPAD_DIVIDE     0x54
#define HID_KEY_KEYPAD_MULTIPLY   0x55
#define HID_KEY_KEYPAD_SUBTRACT   0x56
#define HID_KEY_KEYPAD_ADD        0x57
#define HID_KEY_KEYPAD_ENTER      0x58
#define HID_KEY_KEYPAD_1          0x59
#define HID_KEY_KEYPAD_2          0x5A
#define HID_KEY_KEYPAD_3          0x5B
#define HID_KEY_KEYPAD_4          0x5C
#define HID_KEY_KEYPAD_5          0x5D
#define HID_KEY_KEYPAD_6          0x5E
#define HID_KEY_KEYPAD_7          0x5F
#define HID_KEY_KEYPAD_8          0x60
#define HID_KEY_KEYPAD_9          0x61
#endif

#ifndef HID_USAGE_CONSUMER_VOLUME_INCREMENT
#define HID_USAGE_CONSUMER_VOLUME_INCREMENT 0x00E9
#define HID_USAGE_CONSUMER_VOLUME_DECREMENT 0x00EA
#define HID_USAGE_CONSUMER_MUTE             0x00E2
#endif

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

// ====================================================================
// DUAL-CORE HID IMPLEMENTATION (Mbed OS vs Earle Philhower / TinyUSB)
// ====================================================================

#if defined(ARDUINO_ARCH_MBED) || defined(ARDUINO_ARCH_MBED_RP2040)

#include <Keyboard.h>

void initHID() {
  Keyboard.begin();
}

void sendKeyboardReport(uint8_t* keys, uint8_t count) {
  // Release keys no longer pressed
  Keyboard.releaseAll();
  for (uint8_t i = 0; i < count && i < 6; i++) {
    if (keys[i] != 0) {
      Keyboard.press(keys[i]);
    }
  }
}

void sendConsumerReport(uint16_t code) {
  // Consumer media keys mapping
  if (code == HID_USAGE_CONSUMER_VOLUME_INCREMENT) {
    Keyboard.press(KEY_MEDIA_VOLUME_INC);
    delay(10);
    Keyboard.release(KEY_MEDIA_VOLUME_INC);
  } else if (code == HID_USAGE_CONSUMER_VOLUME_DECREMENT) {
    Keyboard.press(KEY_MEDIA_VOLUME_DEC);
    delay(10);
    Keyboard.release(KEY_MEDIA_VOLUME_DEC);
  } else if (code == HID_USAGE_CONSUMER_MUTE) {
    Keyboard.press(KEY_MEDIA_MUTE);
    delay(10);
    Keyboard.release(KEY_MEDIA_MUTE);
  }
}

#else

// Earle Philhower RP2040 Core using Adafruit TinyUSB
#include <Adafruit_TinyUSB.h>

uint8_t const desc_hid_report[] = {
  TUD_HID_REPORT_DESC_KEYBOARD(HID_REPORT_ID(1)),
  TUD_HID_REPORT_DESC_CONSUMER(HID_REPORT_ID(2))
};

Adafruit_USBD_HID usb_hid;

void initHID() {
  usb_hid.setPollInterval(2);
  usb_hid.setReportDescriptor(desc_hid_report, sizeof(desc_hid_report));
  usb_hid.begin();

  while (!TinyUSBDevice.mounted()) {
    delay(10);
  }
}

void sendKeyboardReport(uint8_t* keys, uint8_t count) {
  if (!usb_hid.ready()) return;
  hid_keyboard_report_t kb_report;
  memset(&kb_report, 0, sizeof(kb_report));
  for (uint8_t i = 0; i < count && i < 6; i++) {
    kb_report.keycode[i] = keys[i];
  }
  usb_hid.sendReport(1, &kb_report, sizeof(kb_report));
}

void sendConsumerReport(uint16_t code) {
  if (!usb_hid.ready()) return;
  usb_hid.sendReport16(2, code);
  delay(10);
  usb_hid.sendReport16(2, 0);
}

#endif

// ====================================================================
// DEFAULT KEYMAP MATRIX (15 Keys + Encoder Slot at Row 0, Col 0)
// ====================================================================

const uint8_t KEYMAP[4][4] = {
  { 0,            HID_KEY_NUM_LOCK,    HID_KEY_KEYPAD_DIVIDE,   HID_KEY_KEYPAD_MULTIPLY },
  { HID_KEY_KEYPAD_7, HID_KEY_KEYPAD_8, HID_KEY_KEYPAD_9,    HID_KEY_KEYPAD_SUBTRACT },
  { HID_KEY_KEYPAD_4, HID_KEY_KEYPAD_5, HID_KEY_KEYPAD_6,    HID_KEY_KEYPAD_ADD },
  { HID_KEY_KEYPAD_1, HID_KEY_KEYPAD_2, HID_KEY_KEYPAD_3,    HID_KEY_KEYPAD_ENTER }
};

int last_encoder_a = HIGH;
bool last_encoder_btn = HIGH;

void setup() {
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

  // Initialize USB HID Subsystem
  initHID();
}

void loop() {
  // ------------------------------------------------------------------
  // 1. Scan 4x4 Key Matrix (15 Mechanical Switches)
  // ------------------------------------------------------------------
  uint8_t key_report[6] = {0};
  uint8_t report_count = 0;

  for (int r = 0; r < 4; r++) {
    for (int c = 0; c < 4; c++) {
      // Row 0, Col 0 is reserved for physical rotary encoder
      if (r == 0 && c == 0) continue;

      digitalWrite(COL_PINS[c], HIGH);
      delayMicroseconds(5);

      bool pressed = (digitalRead(ROW_PINS[r]) == HIGH);
      digitalWrite(COL_PINS[c], LOW);

      if (pressed && report_count < 6) {
        key_report[report_count++] = KEYMAP[r][c];
      }
    }
  }

  // Send HID Keyboard Report
  sendKeyboardReport(key_report, report_count);

  // ------------------------------------------------------------------
  // 2. Scan Rotary Encoder Rotation (Volume Control)
  // ------------------------------------------------------------------
  int current_a = digitalRead(ENCODER_PIN_A);
  if (current_a != last_encoder_a && current_a == LOW) {
    if (digitalRead(ENCODER_PIN_B) == HIGH) {
      sendConsumerReport(HID_USAGE_CONSUMER_VOLUME_INCREMENT);
    } else {
      sendConsumerReport(HID_USAGE_CONSUMER_VOLUME_DECREMENT);
    }
  }
  last_encoder_a = current_a;

  // ------------------------------------------------------------------
  // 3. Scan Rotary Encoder Push Button (Mute Audio)
  // ------------------------------------------------------------------
  bool current_btn = (digitalRead(ENCODER_PIN_BTN) == LOW);
  if (current_btn && !last_encoder_btn) {
    sendConsumerReport(HID_USAGE_CONSUMER_MUTE);
  }
  last_encoder_btn = current_btn;

  delay(5);
}
