# boot.py - CircuitPython USB Configuration
import board
import digitalio
import storage
import usb_hid

# Set USB product name
# storage.remount("/", readonly=False) # Uncomment if you want to allow filesystem writes from Python code

# Enable standard USB HID devices (Keyboard, Consumer Control / Media keys, Mouse)
usb_hid.enable(
    (
        usb_hid.Device.KEYBOARD,
        usb_hid.Device.CONSUMER_CONTROL,
        usb_hid.Device.MOUSE,
    )
)
