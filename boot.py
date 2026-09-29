# boot.py - CircuitPython USB Keyboard Configuration
import board
import digitalio
import storage
import supervisor
import usb_hid

# Set recognizable USB Manufacturer and Product name in OS / Device Manager
supervisor.set_usb_identification(
    manufacturer="Custom Tech",
    product="15-Key RP2040 Macropad",
)

# Enable standard USB HID devices (Keyboard, Consumer Control / Media keys, Mouse)
usb_hid.enable(
    (
        usb_hid.Device.KEYBOARD,
        usb_hid.Device.CONSUMER_CONTROL,
        usb_hid.Device.MOUSE,
    )
)
