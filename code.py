"""
====================================================================
 15-Key + 1 Rotary Encoder Macropad Firmware
 Board: Waveshare RP2040-Zero
 Firmware: CircuitPython + KMK
 Device Name: "15-Key RP2040 Macropad"
====================================================================
"""

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.modules.macros import Press, Release, Tap, Delay, Macros
from kmk.extensions.media_keys import MediaKeys

# Initialize Keyboard
keyboard = KMKKeyboard()
keyboard.name = "15-Key RP2040 Macropad"

# Modules & Extensions
layers = Layers()
encoder_handler = EncoderHandler()
macros = Macros()
media_keys = MediaKeys()

keyboard.modules = [layers, encoder_handler, macros]
keyboard.extensions = [media_keys]

# ====================================================================
# HARDWARE PIN CONFIGURATION
# ====================================================================

# 4x4 Matrix Pin Definitions
keyboard.row_pins = (board.GP0, board.GP1, board.GP2, board.GP3)
keyboard.col_pins = (board.GP4, board.GP5, board.GP6, board.GP7)

# Diode Direction:
# COL2ROW (Anode on Column, Cathode/Stripe on Row)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Rotary Encoder Pins (Encoder A, Encoder B, Push Switch, Is_Flipped)
encoder_handler.pins = ((board.GP8, board.GP9, board.GP10, False),)

# ====================================================================
# CUSTOMIZABLE MACROS & SHORTCUTS
# Create your custom key combinations or text macros here!
# ====================================================================

# Common OS / Productivity Shortcuts
MACRO_COPY      = KC.MACRO(Press(KC.LCTRL), Tap(KC.C), Release(KC.LCTRL))
MACRO_PASTE     = KC.MACRO(Press(KC.LCTRL), Tap(KC.V), Release(KC.LCTRL))
MACRO_CUT       = KC.MACRO(Press(KC.LCTRL), Tap(KC.X), Release(KC.LCTRL))
MACRO_UNDO      = KC.MACRO(Press(KC.LCTRL), Tap(KC.Z), Release(KC.LCTRL))
MACRO_REDO      = KC.MACRO(Press(KC.LCTRL), Tap(KC.Y), Release(KC.LCTRL))
MACRO_SELECT_ALL= KC.MACRO(Press(KC.LCTRL), Tap(KC.A), Release(KC.LCTRL))
MACRO_SAVE      = KC.MACRO(Press(KC.LCTRL), Tap(KC.S), Release(KC.LCTRL))
MACRO_TASK_MGR  = KC.MACRO(Press(KC.LCTRL), Press(KC.LSHIFT), Tap(KC.ESCAPE), Release(KC.LSHIFT), Release(KC.LCTRL))
MACRO_LOCK_PC   = KC.MACRO(Press(KC.LGUI), Tap(KC.L), Release(KC.LGUI))
MACRO_SCREENSHOT= KC.MACRO(Press(KC.LGUI), Press(KC.LSHIFT), Tap(KC.S), Release(KC.LSHIFT), Release(KC.LGUI))

# Example Text Macro
MACRO_MY_EMAIL  = KC.MACRO("user@example.com")


# ====================================================================
# KEYMAP LAYERS
# 16 physical positions in a 4x4 grid.
# Top-Left slot [R0, C0] is physical Rotary Encoder body (assigned KC.NO).
# ====================================================================

# Quick Layer Switch Keys:
# KC.MO(1) -> Hold for Layer 1
# KC.TO(1) -> Toggle to Layer 1
# KC.TT(1) -> Tap-Toggle Layer 1

keyboard.keymap = [
    # ----------------------------------------------------------------
    # LAYER 0: NUMPAD & MEDIA CONTROLS (DEFAULT BASE LAYER)
    # ----------------------------------------------------------------
    # [ (R0,C0: ENCODER),  (R0,C1): Slash,    (R0,C2): Asterisk, (R0,C3): Layer 1 Hold ]
    # [ (R1,C0): Num 7,    (R1,C1): Num 8,    (R1,C2): Num 9,    (R1,C3): Minus        ]
    # [ (R2,C0): Num 4,    (R2,C1): Num 5,    (R2,C2): Num 6,    (R2,C3): Plus         ]
    # [ (R3,C0): Num 1,    (R3,C1): Num 2,    (R3,C2): Num 3,    (R3,C3): Num Enter    ]
    [
        KC.NO,          KC.KP_SLASH,    KC.KP_ASTERISK, KC.MO(1),
        KC.KP_7,        KC.KP_8,        KC.KP_9,        KC.KP_MINUS,
        KC.KP_4,        KC.KP_5,        KC.KP_6,        KC.KP_PLUS,
        KC.KP_1,        KC.KP_2,        KC.KP_3,        KC.KP_ENTER,
    ],

    # ----------------------------------------------------------------
    # LAYER 1: PRODUCTIVITY & MACRO SUITE
    # ----------------------------------------------------------------
    # [ (R0,C0: ENCODER),  (R0,C1): Cut,      (R0,C2): Copy,     (R0,C3): Transparent  ]
    # [ (R1,C0): Sel All,  (R1,C1): Save,     (R1,C2): Paste,    (R1,C3): Screenshot   ]
    # [ (R2,C0): Lock PC,  (R2,C1): TaskMgr,  (R2,C2): Redo,     (R2,C3): Delete       ]
    # [ (R3,C0): Home,     (R3,C1): Email,    (R3,C2): End,      (R3,C3): Undo         ]
    [
        KC.NO,            MACRO_CUT,     MACRO_COPY,     KC.TRNS,
        MACRO_SELECT_ALL, MACRO_SAVE,    MACRO_PASTE,    MACRO_SCREENSHOT,
        MACRO_LOCK_PC,    MACRO_TASK_MGR,MACRO_REDO,     KC.DELETE,
        KC.HOME,          MACRO_MY_EMAIL,KC.END,          MACRO_UNDO,
    ],
]

# ====================================================================
# ROTARY ENCODER BEHAVIOR PER LAYER
# Structure: (( ClockwiseAction, CounterClockwiseAction, PushButtonAction ),)
# ====================================================================
encoder_handler.map = [
    # Layer 0: Volume & Mute (CW: Vol Up, CCW: Vol Down, Push: Mute)
    ((KC.AUDIO_VOL_UP, KC.AUDIO_VOL_DOWN, KC.AUDIO_MUTE),),

    # Layer 1: Mouse Scrolling & Media Play/Pause (CW: Scroll Down, CCW: Scroll Up, Push: Play/Pause)
    ((KC.MW_DN, KC.MW_UP, KC.MEDIA_PLAY_PAUSE),),
]

if __name__ == "__main__":
    keyboard.go()
