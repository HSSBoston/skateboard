import blinkt, time
from colorzero import Color, Hue

color = Color(255, 0, 0) + Hue(deg=10)
blinkt.set_all(color.rgb_bytes[0], color.rgb_bytes[1], color.rgb_bytes[2])
blinkt.show()
time.sleep(2)

color = color + Hue(deg=180)
blinkt.set_all(color.rgb_bytes[0], color.rgb_bytes[1], color.rgb_bytes[2])
blinkt.show()
time.sleep(2)

blinkt.clear()
blinkt.show()
