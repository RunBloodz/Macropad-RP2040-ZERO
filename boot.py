# boot.py - CircuitPython USB Gamepad & HID Configuration
import board
import digitalio
import storage
import supervisor
import usb_hid

# Set USB Manufacturer and Product name recognized in Windows / Linux / macOS
supervisor.set_usb_identification(
    manufacturer="Custom Tech",
    product="15-Key RP2040 Gamepad Controller",
)

# Enable Gamepad, Keyboard, Consumer Control, and Mouse HID descriptors
usb_hid.enable(
    (
        usb_hid.Device.GAMEPAD,
        usb_hid.Device.KEYBOARD,
        usb_hid.Device.CONSUMER_CONTROL,
        usb_hid.Device.MOUSE,
    )
)
