"""
CircuitPython code for testing IR proximity sensor with QT Py RP2040
"""

import time
import board
import digitalio
import neopixel

sensor_pin = board.D0
pixel_pin = board.NEOPIXEL

pixel = neopixel.NeoPixel(pixel_pin, 1)
pixel.brightness = 0.3

sensor = digitalio.DigitalInOut(sensor_pin)
blink = False

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

BLINK_TIME = 0.2
PAUSE_TIME = 0.05

CLOSE = False
FAR = True

print("Pre-loop!")

while True:
    print(sensor.value)

    if sensor.value is FAR:
        pixel.fill(RED)
    else:
        pixel.fill(GREEN)
    time.sleep(BLINK_TIME)
    
    pixel.fill(PURPLE)
    time.sleep(PAUSE_TIME)
    
print("Post-loop! Should never happen BTW")
