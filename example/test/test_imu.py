import struct
import math
import utime
from machine import Pin, I2C
from mpu6050 import MPU6050

if __name__ == "__main__":
    mpu = MPU6050(bus = 0,scl=Pin(9), sda=Pin(8))
    while True:
            g=mpu.readData()
            print("X:{:.2f}  Y:{:.2f}  Z:{:.2f}".format(g.Gx,g.Gy,g.Gz))
            utime.sleep_ms(100)