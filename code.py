"""
15-Key + 1 Rotary Encoder (4x4 Matrix) Macropad Firmware
Powered by CircuitPython & KMK Firmware
Board: RP2040-Zero
"""

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.modules.macros import Press, Release, Tap, Delay, Macros
from kmk.extensions.media_keys import MediaKeys

# Initialize Keyboard instance
keyboard = KMKKeyboard()

# Add Modules & Extensions
layers = Layers()
encoder_handler = EncoderHandler()
macros = Macros()
media_keys = MediaKeys()

keyboard.modules = [layers, encoder_handler, macros]
keyboard.extensions = [media_keys]

# --- HARDWARE CONFIGURATION ---

# 4x4 Matrix Pin Definitions
# Rows 0..3: GP0, GP1, GP2, GP3
# Cols 0..3: GP4, GP5, GP6, GP7
keyboard.row_pins = (board.GP0, board.GP1, board.GP2, board.GP3)
keyboard.col_pins = (board.GP4, board.GP5, board.GP6, board.GP7)

# Diode Direction:
# COL2ROW = Anode on Column, Cathode (striped side) on Row.
# If your diodes are wired ROW2COL, change DiodeOrientation.COL2ROW to DiodeOrientation.ROW2COL
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Rotary Encoder Configuration
# Pin A: GP8, Pin B: GP9
# Push Button: Dedicated pin GP10
encoder_handler.pins = ((board.GP8, board.GP9, board.GP10, False),)

# --- KEYMAP & MACROS CONFIGURATION ---

# Custom Macro Definitions (Easily customizable!)
# Example: Copy / Paste / Undo / Cut / Select All / Custom Shortcut String
MACRO_COPY = KC.MACRO(Press(KC.LCTRL), Tap(KC.C), Release(KC.LCTRL))
MACRO_PASTE = KC.MACRO(Press(KC.LCTRL), Tap(KC.V), Release(KC.LCTRL))
MACRO_CUT = KC.MACRO(Press(KC.LCTRL), Tap(KC.X), Release(KC.LCTRL))
MACRO_UNDO = KC.MACRO(Press(KC.LCTRL), Tap(KC.Z), Release(KC.LCTRL))
MACRO_SELECT_ALL = KC.MACRO(Press(KC.LCTRL), Tap(KC.A), Release(KC.LCTRL))
MACRO_SAVE = KC.MACRO(Press(KC.LCTRL), Tap(KC.S), Release(KC.LCTRL))

# 4x4 Key Matrix Map (16 total positions)
# Note: Position (Row 0, Col 0) is occupied by physical Encoder knob on PCB.
# In keymap array below, key index 0 is assigned KC.NO or layer switch/encoder key.

# --- LAYER DEFINITIONS ---
# Layer 0: Default Numpad & Media Control
# Layer 1: Productivity Macros & Shortcuts (Hold/Tap TO(1) / MO(1) / TT(1) to activate)

_BASE = 0
_MACRO = 1

keyboard.keymap = [
    # LAYER 0: Numpad & Media Layer
    # [ (R0,C0 ENCODER SLOT),  (R0,C1),  (R0,C2),  (R0,C3) ]
    # [ (R1,C0),              (R1,C1),  (R1,C2),  (R1,C3) ]
    # [ (R2,C0),              (R2,C1),  (R2,C2),  (R2,C3) ]
    # [ (R3,C0),              (R3,C1),  (R3,C2),  (R3,C3) ]
    [
        KC.NO,          KC.KP_SLASH, KC.KP_ASTERISK, KC.MO(1),
        KC.KP_7,        KC.KP_8,     KC.KP_9,        KC.KP_MINUS,
        KC.KP_4,        KC.KP_5,     KC.KP_6,        KC.KP_PLUS,
        KC.KP_1,        KC.KP_2,     KC.KP_3,        KC.KP_ENTER,
    ],

    # LAYER 1: Productivity Macros & Function Layer
    [
        KC.NO,          MACRO_CUT,   MACRO_COPY,     KC.TRNS,
        MACRO_SELECT_ALL, MACRO_SAVE, MACRO_PASTE,  KC.DELETE,
        KC.HOME,        KC.UP,       KC.END,         KC.ESCAPE,
        KC.LEFT,        KC.DOWN,     KC.RIGHT,       MACRO_UNDO,
    ],
]

# --- ROTARY ENCODER BEHAVIOR PER LAYER ---
# encoder_handler.map = [
#     [ (Encoder 1 CW, Encoder 1 CCW, Encoder 1 Push) ] -> Layer 0
#     [ (Encoder 1 CW, Encoder 1 CCW, Encoder 1 Push) ] -> Layer 1
# ]
encoder_handler.map = [
    # Layer 0: Volume Control (CW = Vol Up, CCW = Vol Down, Push = Mute/Unmute)
    ((KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN, KC.AUDIO_MUTE),),

    # Layer 1: Page Scrolling / Zooming (CW = Scroll Down, CCW = Scroll Up, Push = Play/Pause)
    ((KC.MW_DN, KC.MW_UP, KC.MEDIA_PLAY_PAUSE),),
]

if __name__ == "__main__":
    keyboard.go()
