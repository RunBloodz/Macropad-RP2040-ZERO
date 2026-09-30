"""
====================================================================
 15-Key + 1 Rotary Encoder + Analog Axis Gamepad Controller
 Board: Waveshare RP2040-Zero
 Firmware: CircuitPython (keypad + rotaryio + analogio + adafruit_tinyusb.hid)
 Device Name: "15-Key RP2040 Gamepad Controller"
====================================================================
"""

import time
import board
import digitalio
import analogio
import keypad
import rotaryio
import microcontroller
import supervisor
import sys
import struct

# TinyUSB & HID imports
try:
    import usb_hid
    import adafruit_tinyusb.hid as tinyusb_hid
    from adafruit_hid.gamepad import Gamepad
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
    from adafruit_hid.consumer_control import ConsumerControl
    from adafruit_hid.consumer_control_code import ConsumerControlCode
    HAS_TINYUSB = True
except ImportError:
    # Fallback to standard usb_hid / adafruit_hid if adafruit_tinyusb module is not on device
    import usb_hid
    from adafruit_hid.gamepad import Gamepad
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode
    from adafruit_hid.consumer_control import ConsumerControl
    from adafruit_hid.consumer_control_code import ConsumerControlCode
    HAS_TINYUSB = False

# Initialize HID Devices via TinyUSB / usb_hid
keyboard = Keyboard(usb_hid.devices) if usb_hid else None
consumer = ConsumerControl(usb_hid.devices) if usb_hid else None

# Find custom Gamepad device descriptor
gamepad_dev = None
if usb_hid:
    for dev in usb_hid.devices:
        if dev.usage_page == 0x01 and dev.usage in (0x04, 0x05): # Joystick or Gamepad usage
            gamepad_dev = dev
            break

if not gamepad_dev and usb_hid:
    try:
        gamepad = Gamepad(usb_hid.devices)
    except Exception:
        gamepad = None
else:
    gamepad = Gamepad([gamepad_dev]) if gamepad_dev else None

# Setup ADC Pin (Analog Axis / Handbrake on GP26)
try:
    handbrake_pin = analogio.AnalogIn(board.GP26)
except Exception as e:
    print(f"BLAD ADC: {e}")
    handbrake_pin = None

# ====================================================================
# NVM CONFIGURATION & PERSISTENT CALIBRATION
# Format: min (H), max (H), dz_start (B), dz_end (B) = 6 bytes
# ====================================================================
CONF_FMT = "<HHBB"
CONF_SIZE = struct.calcsize(CONF_FMT)
config = {"min": 0, "max": 65535, "dz_start": 0, "dz_end": 0}

def load_config():
    global config
    try:
        if microcontroller.nvm[0:CONF_SIZE] != b'\xff' * CONF_SIZE:
            data = microcontroller.nvm[0 : CONF_SIZE]
            min_v, max_v, dzs, dze = struct.unpack(CONF_FMT, data)
            config = {"min": min_v, "max": max_v, "dz_start": dzs, "dz_end": dze}
    except Exception as e:
        print(f"BLAD NVM: {e}")

def save_config():
    try:
        data = struct.pack(CONF_FMT, config["min"], config["max"], config["dz_start"], config["dz_end"])
        microcontroller.nvm[0 : CONF_SIZE] = data
    except Exception as e:
        print(f"BLAD ZAPISU: {e}")

load_config()

# Helper Math Functions
def map_value(val, in_min, in_max, out_min, out_max):
    if in_max == in_min:
        return out_min
    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def constrain(val, min_v, max_v):
    return max(min(val, max_v), min_v)

def process_handbrake(raw, cfg):
    min_v = cfg["min"]
    max_v = cfg["max"]
    if min_v == max_v:
        return -32768
    range_v = max_v - min_v
    start_v = int(min_v + (range_v * cfg["dz_start"] / 100))
    end_v = int(max_v - (range_v * cfg["dz_end"] / 100))
    if min_v < max_v:
        val = constrain(raw, start_v, end_v)
        return map_value(val, start_v, end_v, -32768, 32767)
    else:
        val = constrain(raw, end_v, start_v)
        return map_value(val, start_v, end_v, -32768, 32767)

# ====================================================================
# HARDWARE PIN CONFIGURATION
# ====================================================================

# 4x4 Matrix Configuration (RP2040-Zero Pins)
ROW_PINS = (board.GP0, board.GP1, board.GP2, board.GP3)
COL_PINS = (board.GP4, board.GP5, board.GP6, board.GP7)

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
# GAMEPAD KEYMAP CONFIGURATION
# ====================================================================

current_layer = 0
pressed_key_actions = {}

KEYMAP = {
    # ----------------------------------------------------------------
    # PROFILE 0: STANDARD GAMEPAD CONTROLLER
    # ----------------------------------------------------------------
    0: [
        ('NONE', None),         # Index 0 (Encoder Slot)
        ('GAMEPAD', 1),         # Index 1
        ('GAMEPAD', 2),         # Index 2
        ('LAYER_HOLD', 1),      # Index 3 - Layer Switch
        ('GAMEPAD', 3),         # Index 4
        ('GAMEPAD', 4),         # Index 5
        ('GAMEPAD', 5),         # Index 6
        ('GAMEPAD', 6),         # Index 7
        ('GAMEPAD', 7),         # Index 8
        ('GAMEPAD', 8),         # Index 9
        ('GAMEPAD', 9),         # Index 10
        ('GAMEPAD', 10),        # Index 11
        ('GAMEPAD', 11),        # Index 12
        ('GAMEPAD', 12),        # Index 13
        ('GAMEPAD', 13),        # Index 14
        ('GAMEPAD', 14),        # Index 15
    ],

    # ----------------------------------------------------------------
    # PROFILE 1: SECONDARY GAMEPAD / KEYBOARD HOTKEYS
    # ----------------------------------------------------------------
    1: [
        ('NONE', None),
        ('GAMEPAD', 15),
        ('GAMEPAD', 16),
        ('LAYER_HOLD', 1),
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

joystick_x = 0  # Steering Range -127 to 127
last_z_val = None
serial_buffer = ""

print("RP2040 Gamepad Controller (Adafruit TinyUSB) Ready. Protocol: 1.1 (Signed Z)")

# ====================================================================
# MAIN LOOP
# ====================================================================

while True:
    # 1. Read Potentiometer / Analog Axis on GP26
    current_raw = 0
    if handbrake_pin:
        raw_sum = 0
        for _ in range(8):
            raw_sum += handbrake_pin.value
        current_raw = raw_sum // 8

    # Process handbrake Z signed value (-32768 to 32767)
    z_val = process_handbrake(current_raw, config)

    # Update Gamepad Z-Axis / Joystick
    if gamepad and (z_val != last_z_val):
        last_z_val = z_val
        z_hid = map_value(z_val, -32768, 32767, -127, 127)
        try:
            gamepad.move_joysticks(x=joystick_x, z=z_hid)
        except TypeError:
            try:
                gamepad.move_joysticks(x=joystick_x, r_z=z_hid)
            except Exception:
                pass
        except Exception:
            pass

    # 2. Process Key Matrix Events
    event = matrix.events.get()
    if event:
        key_number = event.key_number
        if event.pressed:
            layer_map = KEYMAP.get(current_layer, KEYMAP[0])
            action_type, action_val = layer_map[key_number]
            pressed_key_actions[key_number] = (action_type, action_val)

            if action_type == 'GAMEPAD' and gamepad:
                gamepad.press_buttons(action_val)
            elif action_type == 'KEY' and keyboard:
                keyboard.press(action_val)
            elif action_type == 'LAYER_HOLD':
                current_layer = action_val

        elif event.released:
            action_type, action_val = pressed_key_actions.pop(key_number, ('NONE', None))

            if action_type == 'GAMEPAD' and gamepad:
                gamepad.release_buttons(action_val)
            elif action_type == 'KEY' and keyboard:
                keyboard.release(action_val)
            elif action_type == 'LAYER_HOLD':
                current_layer = 0

    # 3. Process Rotary Encoder Rotation
    current_encoder_position = encoder.position
    if current_encoder_position != last_encoder_position:
        diff = current_encoder_position - last_encoder_position
        last_encoder_position = current_encoder_position

        if current_layer == 0:
            joystick_x = max(-127, min(127, joystick_x + (diff * 15)))
            if gamepad:
                z_hid = map_value(z_val, -32768, 32767, -127, 127)
                try:
                    gamepad.move_joysticks(x=joystick_x, z=z_hid)
                except Exception:
                    pass
        else:
            if consumer:
                if diff > 0:
                    consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
                else:
                    consumer.send(ConsumerControlCode.VOLUME_DECREMENT)

    # 4. Process Encoder Push Button
    current_button_state = encoder_button.value
    if current_button_state != last_button_state:
        last_button_state = current_button_state
        if not current_button_state:
            if current_layer == 0 and gamepad:
                gamepad.press_buttons(16)
            elif consumer:
                consumer.send(ConsumerControlCode.MUTE)
        else:
            if current_layer == 0 and gamepad:
                gamepad.release_buttons(16)

    # 5. Handle Serial Commands (Non-blocking Calibration & Debug Protocol)
    if supervisor.runtime.serial_bytes_available:
        char = sys.stdin.read(1)
        if char == "\n" or char == "\r":
            cmd = serial_buffer.strip()
            serial_buffer = ""
            if cmd == "READ":
                print(f"RAW:{current_raw}")
            elif cmd == "PING":
                print("PONG")
            elif cmd == "GET_CONFIG":
                print(f"CONF:{config['min']}:{config['max']}:{config['dz_start']}:{config['dz_end']}")
            elif cmd.startswith("SET"):
                try:
                    parts = cmd.split()
                    if len(parts) == 5:
                        config = {
                            "min": int(parts[1]),
                            "max": int(parts[2]),
                            "dz_start": int(parts[3]),
                            "dz_end": int(parts[4])
                        }
                        print("OK")
                except Exception:
                    print("SET_ERR")
            elif cmd == "SAVE":
                save_config()
                print("SAVED")
        else:
            serial_buffer += char
            if len(serial_buffer) > 100:
                serial_buffer = ""

    time.sleep(0.01)
