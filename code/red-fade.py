import blinkt, time
x = 0
while True:
    try:
        while x < 1:
            blinkt.set_all(255, 0, 0, x)
            blinkt.show()
            time.sleep(0.01)
            x = x + 0.1

        x = 1
        while x > 0:
            blinkt.set_all(255, 0, 0, x)
            blinkt.show()
            time.sleep(0.01)
            x = x - 0.1
        x = 0
    except KeyboardInterrupt:
        break

blinkt.clear()
blinkt.show()