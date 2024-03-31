import blinkt, time
from colorzero import Color, Hue

orange = Color(255, 0, 0) + Hue(deg=10)
teal = orange + Hue(deg=180)

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

while True:
    try:
        fadeInOut(orange)
        fadeInOut(teal)
    except KeyboardInterrupt:
        break

blinkt.clear()
blinkt.show()
