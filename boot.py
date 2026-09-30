# boot.py - CircuitPython USB Setup with Adafruit TinyUSB / USB HID
import board
import digitalio
import storage
import supervisor
import usb_hid

# Set USB Manufacturer and Product name
supervisor.set_usb_identification(
    manufacturer="Custom Tech",
    product="15-Key RP2040 Gamepad Controller",
)

# Enable standard Gamepad, Keyboard, Consumer Control, and Mouse HID interfaces
usb_hid.enable(
    (
        usb_hid.Device.GAMEPAD,
        usb_hid.Device.KEYBOARD,
        usb_hid.Device.CONSUMER_CONTROL,
        usb_hid.Device.MOUSE,
    )
)
