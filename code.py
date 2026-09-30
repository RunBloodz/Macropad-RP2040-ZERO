"""
====================================================================
 15-Key + 1 Rotary Encoder Gamepad Controller Firmware
 Board: Waveshare RP2040-Zero
 Firmware: CircuitPython Gamepad (keypad + rotaryio + adafruit_hid)
 Device Name: "15-Key RP2040 Gamepad Controller"
====================================================================
"""

import time
import board
import digitalio
import keypad
import rotaryio
import usb_hid

# Import HID Gamepad, Keyboard, and Consumer Control
from adafruit_hid.gamepad import Gamepad
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Find USB Gamepad device descriptor
gamepad_device = None
for device in usb_hid.devices:
    if device.usage == 0x05 and device.usage_page == 0x01: # Gamepad usage
        gamepad_device = device
        break

if gamepad_device is None:
    # Fallback to standard Gamepad initialization if found in devices
    try:
        gamepad = Gamepad(usb_hid.devices)
    except Exception:
        gamepad = None
else:
    gamepad = Gamepad([gamepad_device])

keyboard = Keyboard(usb_hid.devices)
consumer = ConsumerControl(usb_hid.devices)

# ====================================================================
# HARDWARE PIN CONFIGURATION
# ====================================================================

# 4x4 Matrix Configuration (RP2040-Zero Pins)
ROW_PINS = (board.GP0, board.GP1, board.GP2, board.GP3)
COL_PINS = (board.GP4, board.GP5, board.GP6, board.GP7)

# keypad.KeyMatrix handles debouncing and diode matrix (COL2ROW)
matrix = keypad.KeyMatrix(
    row_pins=ROW_PINS,
    column_pins=COL_PINS,
    columns_to_anodes=True,
)

# Rotary Encoder Hardware Setup (GP8, GP9)
encoder = rotaryio.IncrementalEncoder(board.GP8, board.GP9)
last_encoder_position = encoder.position

# Rotary Encoder Push Button Setup (GP10)
encoder_button = digitalio.DigitalInOut(board.GP10)
encoder_button.direction = digitalio.Direction.INPUT
encoder_button.pull = digitalio.Pull.UP
last_button_state = True

# ====================================================================
# GAMEPAD & KEYMAP CONFIGURATION
# 16 physical positions in a 4x4 grid.
# Slot 0 [Row 0, Col 0] is the Rotary Encoder body.
# ====================================================================

# Action types:
# ('GAMEPAD', btn_number) -> Gamepad Button 1 to 16
# ('DPAD', x_val, y_val)  -> D-Pad / Joystick Direction
# ('KEY', Keycode.X)     -> Keyboard Key
# ('LAYER_HOLD', layer)  -> Hold to switch Gamepad Profile Layer
# ('NONE', None)         -> Reserved slot

current_layer = 0
pressed_key_actions = {}

KEYMAP = {
    # ----------------------------------------------------------------
    # PROFILE 0: STANDARD GAMEPAD CONTROLLER
    # Buttons 1..15 corresponding to matrix keys
    # ----------------------------------------------------------------
    0: [
        ('NONE', None),         # Index 0 (R0, C0) - Rotary Encoder Slot
        ('GAMEPAD', 1),         # Index 1 (R0, C1) - Gamepad Button 1 (e.g. A / Cross)
        ('GAMEPAD', 2),         # Index 2 (R0, C2) - Gamepad Button 2 (e.g. B / Circle)
        ('LAYER_HOLD', 1),      # Index 3 (R0, C3) - Layer Switch (Hold for Profile 1)
        ('GAMEPAD', 3),         # Index 4 (R1, C0) - Gamepad Button 3 (e.g. X / Square)
        ('GAMEPAD', 4),         # Index 5 (R1, C1) - Gamepad Button 4 (e.g. Y / Triangle)
        ('GAMEPAD', 5),         # Index 6 (R1, C2) - Gamepad Button 5 (e.g. L1 / LB)
        ('GAMEPAD', 6),         # Index 7 (R1, C3) - Gamepad Button 6 (e.g. R1 / RB)
        ('GAMEPAD', 7),         # Index 8 (R2, C0) - Gamepad Button 7 (e.g. L2 / LT)
        ('GAMEPAD', 8),         # Index 9 (R2, C1) - Gamepad Button 8 (e.g. R2 / RT)
        ('GAMEPAD', 9),         # Index 10 (R2, C2) - Gamepad Button 9 (Select / Back)
        ('GAMEPAD', 10),        # Index 11 (R2, C3) - Gamepad Button 10 (Start)
        ('GAMEPAD', 11),        # Index 12 (R3, C0) - Gamepad Button 11 (L3)
        ('GAMEPAD', 12),        # Index 13 (R3, C1) - Gamepad Button 12 (R3)
        ('GAMEPAD', 13),        # Index 14 (R3, C2) - Gamepad Button 13 (Home)
        ('GAMEPAD', 14),        # Index 15 (R3, C3) - Gamepad Button 14
    ],

    # ----------------------------------------------------------------
    # PROFILE 1: SIM RACING / FLIGHT / HOTKEY GAMEPAD
    # ----------------------------------------------------------------
    1: [
        ('NONE', None),         # Index 0
        ('GAMEPAD', 15),        # Gamepad Button 15
        ('GAMEPAD', 16),        # Gamepad Button 16
        ('LAYER_HOLD', 1),      # Index 3
        ('KEY', Keycode.UP_ARROW),
        ('KEY', Keycode.DOWN_ARROW),
        ('KEY', Keycode.LEFT_ARROW),
        ('KEY', Keycode.RIGHT_ARROW),
        ('KEY', Keycode.SPACEBAR),
        ('KEY', Keycode.LEFT_SHIFT),
        ('KEY', Keycode.LEFT_CONTROL),
        ('KEY', Keycode.ESCAPE),
        ('KEY', Keycode.ENTER),
        ('KEY', Keycode.TAB),
        ('KEY', Keycode.C),
        ('KEY', Keycode.V),
    ],
}

# Joystick Axis position tracking for Rotary Encoder
joystick_x = 0  # Range -127 to 127

print("RP2040 Gamepad Controller Ready!")

# ====================================================================
# MAIN EVENT LOOP
# ====================================================================

while True:
    # 1. Process Keypad Matrix Events
    event = matrix.events.get()
    if event:
        key_number = event.key_number

        if event.pressed:
            layer_map = KEYMAP.get(current_layer, KEYMAP[0])
            action_type, action_val = layer_map[key_number]
            pressed_key_actions[key_number] = (action_type, action_val)

            if action_type == 'GAMEPAD' and gamepad:
                gamepad.press_buttons(action_val)
            elif action_type == 'KEY':
                keyboard.press(action_val)
            elif action_type == 'LAYER_HOLD':
                current_layer = action_val

        elif event.released:
            action_type, action_val = pressed_key_actions.pop(key_number, ('NONE', None))

            if action_type == 'GAMEPAD' and gamepad:
                gamepad.release_buttons(action_val)
            elif action_type == 'KEY':
                keyboard.release(action_val)
            elif action_type == 'LAYER_HOLD':
                current_layer = 0

    # 2. Process Rotary Encoder Rotation (Simulates Steering / Throttle Axis or Volume)
    current_encoder_position = encoder.position
    if current_encoder_position != last_encoder_position:
        diff = current_encoder_position - last_encoder_position
        last_encoder_position = current_encoder_position

        if current_layer == 0:
            # Profile 0: Move Gamepad X-Axis (Steering / Direction)
            joystick_x = max(-127, min(127, joystick_x + (diff * 15)))
            if gamepad:
                gamepad.move_joysticks(x=joystick_x)
        else:
            # Profile 1: Volume adjustment
            if diff > 0:
                consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
            else:
                consumer.send(ConsumerControlCode.VOLUME_DECREMENT)

    # 3. Process Encoder Push Button (Gamepad Button 16 or Mute)
    current_button_state = encoder_button.value
    if current_button_state != last_button_state:
        last_button_state = current_button_state
        if not current_button_state:  # Pressed
            if current_layer == 0 and gamepad:
                gamepad.press_buttons(16)
            else:
                consumer.send(ConsumerControlCode.MUTE)
        else:  # Released
            if current_layer == 0 and gamepad:
                gamepad.release_buttons(16)

    time.sleep(0.001)
