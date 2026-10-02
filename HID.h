#ifndef HID_H
#define HID_H

#include <Arduino.h>

// Dummy HID interface definitions for compatibility
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

#endif
