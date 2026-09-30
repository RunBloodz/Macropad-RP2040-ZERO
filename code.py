"""
====================================================================
 15-Key + 1 Rotary Encoder Macropad Firmware
 Board: Waveshare RP2040-Zero
 Firmware: Pure CircuitPython (keypad + rotaryio + adafruit_hid)
 Device Name: "15-Key RP2040 Macropad"
====================================================================
"""

import time
import board
import digitalio
import keypad
import rotaryio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse

# Initialize HID Devices
keyboard = Keyboard(usb_hid.devices)
consumer = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

# ====================================================================
# HARDWARE PIN CONFIGURATION
# ====================================================================

# 4x4 Matrix Configuration (RP2040-Zero Pins)
ROW_PINS = (board.GP0, board.GP1, board.GP2, board.GP3)
COL_PINS = (board.GP4, board.GP5, board.GP6, board.GP7)

# keypad.KeyMatrix automatically handles debouncing and diode matrices!
# columns_to_anodes=True matches DiodeOrientation.COL2ROW (Anode on Column, Cathode on Row)
matrix = keypad.KeyMatrix(
    row_pins=ROW_PINS,
    column_pins=COL_PINS,
    columns_to_anodes=True,
)

# Rotary Encoder Hardware Setup
# Encoder A: GP8, Encoder B: GP9
encoder = rotaryio.IncrementalEncoder(board.GP8, board.GP9)
last_encoder_position = encoder.position

# Rotary Encoder Push Button Setup (GP10)
encoder_button = digitalio.DigitalInOut(board.GP10)
encoder_button.direction = digitalio.Direction.INPUT
encoder_button.pull = digitalio.Pull.UP
last_button_state = True

# ====================================================================
# MACROS AND CUSTOM ACTIONS
# ====================================================================

def send_shortcut(modifier, key):
    """Utility function to press a key combo like Ctrl+C."""
    keyboard.press(modifier, key)
    time.sleep(0.01)
    keyboard.release_all()

# Active Layer Tracking (0 = Default Base Layer, 1 = Macro Layer)
current_layer = 0

# Track active key action types by key_number to ensure correct release
pressed_key_actions = {}

# ====================================================================
# KEYMAP DEFINITIONS
# Grid 4x4 (Indices 0..15). Index 0 [Row 0, Col 0] is the Encoder position.
# ====================================================================

# Action types:
# ('KEY', Keycode.X) -> Standard Keycode
# ('COMBO', Modifier, Keycode) -> Shortcut Combination
# ('CONSUMER', ConsumerControlCode) -> Media Key
# ('LAYER_HOLD', layer_num) -> Hold for Layer Switch
# ('NONE', None) -> Disabled slot

KEYMAP = {
    # ----------------------------------------------------------------
    # LAYER 0: NUMPAD & BASE CONTROLS
    # ----------------------------------------------------------------
    0: [
        ('NONE', None),                         # Index 0 (R0, C0) - Physical Encoder slot
        ('KEY', Keycode.KEYPAD_FORWARD_SLASH),  # Index 1 (R0, C1)
        ('KEY', Keycode.KEYPAD_ASTERISK),       # Index 2 (R0, C2)
        ('LAYER_HOLD', 1),                      # Index 3 (R0, C3) - Hold for Layer 1
        ('KEY', Keycode.KEYPAD_SEVEN),          # Index 4 (R1, C0)
        ('KEY', Keycode.KEYPAD_EIGHT),          # Index 5 (R1, C1)
        ('KEY', Keycode.KEYPAD_NINE),           # Index 6 (R1, C2)
        ('KEY', Keycode.KEYPAD_MINUS),          # Index 7 (R1, C3)
        ('KEY', Keycode.KEYPAD_FOUR),           # Index 8 (R2, C0)
        ('KEY', Keycode.KEYPAD_FIVE),           # Index 9 (R2, C1)
        ('KEY', Keycode.KEYPAD_SIX),            # Index 10 (R2, C2)
        ('KEY', Keycode.KEYPAD_PLUS),           # Index 11 (R2, C3)
        ('KEY', Keycode.KEYPAD_ONE),            # Index 12 (R3, C0)
        ('KEY', Keycode.KEYPAD_TWO),            # Index 13 (R3, C1)
        ('KEY', Keycode.KEYPAD_THREE),          # Index 14 (R3, C2)
        ('KEY', Keycode.KEYPAD_ENTER),          # Index 15 (R3, C3)
    ],

    # ----------------------------------------------------------------
    # LAYER 1: PRODUCTIVITY MACROS
    # ----------------------------------------------------------------
    1: [
        ('NONE', None),                         # Index 0
        ('COMBO', Keycode.CONTROL, Keycode.X),  # Cut
        ('COMBO', Keycode.CONTROL, Keycode.C),  # Copy
        ('LAYER_HOLD', 1),                      # Index 3 - Keep Layer 1 active while held
        ('COMBO', Keycode.CONTROL, Keycode.A),  # Select All
        ('COMBO', Keycode.CONTROL, Keycode.S),  # Save
        ('COMBO', Keycode.CONTROL, Keycode.V),  # Paste
        ('COMBO', Keycode.GUI, Keycode.PRINT_SCREEN), # Screenshot
        ('COMBO', Keycode.GUI, Keycode.L),      # Lock Screen
        ('COMBO', Keycode.CONTROL, Keycode.Y),  # Redo
        ('KEY', Keycode.DELETE),                # Delete
        ('KEY', Keycode.HOME),                  # Home
        ('KEY', Keycode.END),                   # End
        ('KEY', Keycode.PAGE_DOWN),             # Page Down
        ('KEY', Keycode.PAGE_UP),               # Page Up
        ('COMBO', Keycode.CONTROL, Keycode.Z),  # Undo
    ],
}

# ====================================================================
# MAIN EVENT LOOP
# ====================================================================

print("RP2040 Macropad Ready!")

while True:
    # 1. Process Matrix Key Events
    event = matrix.events.get()
    if event:
        key_number = event.key_number

        if event.pressed:
            # Look up action in the active layer map
            layer_map = KEYMAP.get(current_layer, KEYMAP[0])
            action_type, action_val = layer_map[key_number]

            # Store pressed action so release uses the exact same action
            pressed_key_actions[key_number] = (action_type, action_val)

            if action_type == 'KEY':
                keyboard.press(action_val)
            elif action_type == 'COMBO':
                send_shortcut(action_val[0], action_val[1])
            elif action_type == 'CONSUMER':
                consumer.send(action_val)
            elif action_type == 'LAYER_HOLD':
                current_layer = action_val

        elif event.released:
            # Retrieve the action that was triggered when pressed
            action_type, action_val = pressed_key_actions.pop(key_number, ('NONE', None))

            if action_type == 'KEY':
                keyboard.release(action_val)
            elif action_type == 'LAYER_HOLD':
                current_layer = 0

    # 2. Process Rotary Encoder Rotation
    current_encoder_position = encoder.position
    if current_encoder_position != last_encoder_position:
        diff = current_encoder_position - last_encoder_position
        last_encoder_position = current_encoder_position

        if current_layer == 0:
            # Layer 0: Volume Control
            if diff > 0:
                consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
            else:
                consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
        else:
            # Layer 1: Mouse Scroll
            if diff > 0:
                mouse.move(wheel=-1)
            else:
                mouse.move(wheel=1)

    # 3. Process Rotary Encoder Button Click
    current_button_state = encoder_button.value
    if current_button_state != last_button_state:
        last_button_state = current_button_state
        if not current_button_state:  # Button Pressed (Low)
            if current_layer == 0:
                consumer.send(ConsumerControlCode.MUTE)
            else:
                consumer.send(ConsumerControlCode.PLAY_PAUSE)

    time.sleep(0.001)
