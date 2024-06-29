# Blinkt! driver: https://github.com/pimoroni/blinkt
# Blinkt! pinout: https://pinout.xyz/pinout/blinkt

import blinkt, time, math
from colorzero import Color, Hue
from lis3dh import LIS3DH

sensor = LIS3DH()
orange = Color(255, 0, 0) + Hue(deg=10)
teal = orange + Hue(deg=180)
red = Color(255, 0, 0)

def fadeInOut(color):
    x = 0
    while x < 1:
            blinkt.set_all(color.rgb_bytes[0],
                           color.rgb_bytes[1],
                           color.rgb_bytes[2], x)
            blinkt.show()
            time.sleep(0.01)
            x = x + 0.1
    x = 1
    while x > 0:
        blinkt.set_all(color.rgb_bytes[0],
                       color.rgb_bytes[1],
                       color.rgb_bytes[2], x)
        blinkt.show()
        time.sleep(0.01)
        x = x - 0.1
    x = 0

def rainbowBlink(color):
    i = 0
    while i <= 7 :
       blinkt.set_pixel(i, color.rgb_bytes[0],
                           color.rgb_bytes[1],
                           color.rgb_bytes[2], 1)
       color = color + Hue(deg=45)
       i = i + 1
    for x in range(5):
        blinkt.show()
        time.sleep(0.1)
        blinkt.clear()

def findPitch():
    x, y, z = sensor.readG()
    pitch, roll = sensor.pitchRoll(x, y, -z)
    pitch = math.degrees(pitch)
    return pitch

while True:
    try:
        pitch = findPitch()
        if pitch >= 5 or pitch <= -5:
            rainbowBlink(red)
        else:
            fadeInOut(orange)
            fadeInOut(teal)
    except KeyboardInterrupt:
        break

blinkt.clear()
blinkt.show()
