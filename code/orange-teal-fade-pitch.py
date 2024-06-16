import blinkt, time, math
from colorzero import Color, Hue
from lis3dh import LIS3DH

sensor = LIS3DH()
orange = Color(255, 0, 0) + Hue(deg=10)
teal = orange + Hue(deg=180)

def pitch():
    x, y, z = sensor.readG()
    pitch, roll = sensor.pitchRoll(x, y, -z)
    return math.degrees(pitch)
    
def fadeInOut(color):
    x = 0
    while x < 1:
            blinkt.set_all(color.rgb_bytes[0], color.rgb_bytes[1], color.rgb_bytes[2], x)
            blinkt.show()
            time.sleep(0.01)
            x = x + 0.1
    x = 1
    while x > 0:
        blinkt.set_all(color.rgb_bytes[0], color.rgb_bytes[1], color.rgb_bytes[2], x)
        blinkt.show()
        time.sleep(0.01)
        x = x - 0.1
    x = 0

def fadeInOutRainbow():
    color = Color(255, 0, 0)
    for onCount in range(3):
        for i in range(8):
            blinkt.set_pixel(i, color.rgb_bytes[0], color.rgb_bytes[1], color.rgb_bytes[2], 1)
            color = color + Hue(deg=360/8)
        blinkt.show()
        time.sleep(0.1)
        blinkt.clear()
        blinkt.show()
        
while True:
    try:
        p = pitch()
        if p > 10 or p < -10:
            fadeInOutRainbow()
        else:
            fadeInOut(orange)
            fadeInOut(teal)
    except KeyboardInterrupt:
        break

blinkt.clear()
blinkt.show()
