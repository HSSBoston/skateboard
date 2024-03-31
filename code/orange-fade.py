import blinkt, time
from colorzero import Color, Hue

x = 0
while True:
    try:
        while x < 1:
            color = Color(255, 0, 0) + Hue(deg=10)
            blinkt.set_all(color.rgb_bytes[0], color.rgb_bytes[1], color.rgb_bytes[2], x)
            blinkt.show()
            time.sleep(0.01)
            x = x + 0.1

        x = 1
        while x > 0:
            color = Color(255, 0, 0) + Hue(deg=10)
            blinkt.set_all(color.rgb_bytes[0], color.rgb_bytes[1], color.rgb_bytes[2], x)
            blinkt.show()
            time.sleep(0.01)
            x = x - 0.1
        x = 0
    except KeyboardInterrupt:
        break

blinkt.clear()
blinkt.show()