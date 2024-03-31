import blinkt, time

blinkt.set_pixel(1, 255, 0, 0)
blinkt.set_pixel(0, 0, 255, 0)
blinkt.show()
time.sleep(2)

blinkt.clear()
blinkt.show()
time.sleep(2)

blinkt.set_all(255, 0, 0, 0.5)
blinkt.show()
time.sleep(2)

blinkt.clear()
blinkt.show()