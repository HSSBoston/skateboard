import time, math
from lis3dh import LIS3DH

sensor = LIS3DH()

while True:
    try:
        x, y, z = sensor.readG()
        print(x, y, -z)
        pitch, roll = sensor.pitchRoll(x, y, -z)
        print(math.degrees(pitch))
        print("")
        time.sleep(1)
    except KeyboardInterrupt:
        break
