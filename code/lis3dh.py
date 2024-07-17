# Driver for the LIS3DH accelerometer
# May 31, 2024 v0.06
# IoT for Kids: https://jxsboston.github.io/IoT-Kids/
#
# Use --ignore-missing-imports to run mypy.

import smbus, sys, time, math
from typing import Tuple, Final

_ADDRESS: Final[int] = 0x18  # Default I2C address for LIS3DH
_SCALE:   Final[int] = 2     # Default sensing full-scale: ±2g
                             #   Value choices: 2, 4, 8 or 16

# Register addresses
_REG_WHO_AM_I: Final[int] = 0x0F
_CTRL_REG1:    Final[int] = 0x20
_CTRL_REG2:    Final[int] = 0x21
_CTRL_REG3:    Final[int] = 0x22
_CTRL_REG4:    Final[int] = 0x23
_CTRL_REG5:    Final[int] = 0x24

# Defaults to the high resolution data model and 200Hz data rate
#
class LIS3DH:
    def __init__(self,
                 address: int = _ADDRESS,  # I2C address in hex
                 scale:   int = _SCALE     # Sensing full-scale: 2, 4, 8 or 16
                 ) -> None:
        assert scale in [2, 4, 8, 16], "Wrong LIS3DH sensing full-scale: " +\
               str(scale) + "." + " It must be 2, 4, 8 or 16."

        self._scale: int         = scale
        self._addr:  int         = address
        self._i2c:   smbus.SMBus = smbus.SMBus(1)

        if   self._scale == 2: scaleHex = 0x08
        elif self._scale == 4: scaleHex = 0x18
        elif self._scale == 8: scaleHex = 0x28
        elif self._scale == 16:scaleHex = 0x38

        try:
            # Ping the sensor
            sensorId = self._i2c.read_byte_data(self._addr, _REG_WHO_AM_I)
            if sensorId != 0x33:
                raise RuntimeError("Failed to find a LIS3DH.")
            # Clear the sensor's memory
            self._i2c.write_byte_data(self._addr, _CTRL_REG5, 0x80)
            # Set the default data rate (200 Hz) and enable X, Y and Z axes
            self._i2c.write_byte_data(self._addr, _CTRL_REG1, 0x67)
            # Set sensing full-scale
            self._i2c.write_byte_data(self._addr, _CTRL_REG4, scaleHex)
            print("LIS3DH configured with " + "addr=" + hex(self._addr) +\
                  ", sensing scale=±" + str(self._scale) + "g.")
        except OSError:
            print("Wrong I2C address: " + hex(self._addr))
            raise

    # Returns an I2C address in hex (string).
    def addr(self) -> str:
        return hex(self._addr)

    def scale(self) -> int:
        return self._scale

    def i2c(self) -> smbus.SMBus:
        return self._i2c

    # Read X, Y, and Z acceleration values in G and return them as a tuple.
    # When one of the axes points straight to Earth, its G value is 1 or -1. 
    #
    def readG(self) -> Tuple[float, float, float]:
        # xh: Most significant part of acceleration data
        # xl: Least significant part of acceleration data
        xl = self._i2c.read_byte_data(self._addr, 0x28)
        xh = self._i2c.read_byte_data(self._addr, 0x29)
        yl = self._i2c.read_byte_data(self._addr, 0x2A)
        yh = self._i2c.read_byte_data(self._addr, 0x2B)
        zl = self._i2c.read_byte_data(self._addr, 0x2C)
        zh = self._i2c.read_byte_data(self._addr, 0x2D)
        
        # Concat xh (8-bits) and xl (8 bits) to derive the complete 16-bit accel data. 
        # Its left-justified 12 bits encode an accel value in the default high-res
        # data mode.
        x = (xh << 8 | xl) >> 4
        y = (yh << 8 | yl) >> 4
        z = (zh << 8 | zl) >> 4
        
        # Each accel value is expressed as two's complement. Convert it
        # to a signed value [-2048, 2047]. Note: 2^12 = 4096
        if x >= 2048: x -= 4096
        if y >= 2048: y -= 4096
        if z >= 2048: z -= 4096
        
        # Convert accel values to G values based on the sensing full-scale.
        fullScaleRange = 2 * self._scale
        sensitivity = fullScaleRange/4096
        return (x * sensitivity, y * sensitivity, z * sensitivity)

    # Read X, Y, and Z acceleration values in m/s^2 and return them as a tuple.
    # When one of the axes points straight to Earth, its accel value is 9.806 or -9.806. 
    #
    def read(self) -> Tuple[float, float, float]:
        x, y, z = self.readG()
        return (x * 9.806, y * 9.806, z * 9.806)
    
    # Take X, Y, and Z acceleration values (in either G or m/s^2) and
    # return pitch and roll angles in radian. 
    #
    def pitchRoll(self, x: float, y: float, z: float) -> Tuple[float, float]:
        accelStrength = math.sqrt(x**2 + y**2 + z**2)
        xNormalized = x/accelStrength
        yNormalized = y/accelStrength
        pitch = math.asin(-xNormalized)
        roll = math.asin(yNormalized/math.cos(pitch))
        return (pitch, roll)
        
if __name__ == "__main__":
    sensor = LIS3DH()
    print("g:", sensor.readG() )
    print("m/s^2:", sensor.read() )
    
    x, y, z = sensor.readG()
    pitch, roll = sensor.pitchRoll(x, y, z)
    print("Pitch (degrees):", math.degrees(pitch), "Roll (degrees):", math.degrees(roll))
