# Simple graphic level, read inclination angle with MPU6050.
# Insert MaBee MPU6050 to CN3

import struct
import math
import utime
from machine import SPI, Pin, I2C
from mpu6050 import MPU6050
from ST7735 import TFT
from sysfont import sysfont


spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
# def __init__( self, spi, aDC, aReset, aCS) :
tft = TFT(spi, 14, 15, 13)
mpu = MPU6050(bus=0, scl=Pin(9), sda=Pin(8))


def main():
    tft.initg()
    tft.rgb(True)
    tft.fill(TFT.BLACK)
    tft.text((30, 0), "X Direct", TFT.WHITE, sysfont, 1, nowrap=True)
    tft.rotation(1)
    tft.text((30, 0), "Y Direct", TFT.WHITE, sysfont, 1, nowrap=True)
    tft.rotation(0)
    
    last_Gx, last_Gy = 64, 64

    while True:
        g = mpu.readData()
        Gx, Gy = (int)(64 + g.Gx * 30), (int)(64 + g.Gy * -30)

        if last_Gx != Gx and last_Gy != Gy:
            tft.circle((last_Gx, last_Gy), 15, TFT.BLACK)
            tft.circle((Gx, Gy), 15, TFT.RED)

            last_Gx, last_Gy = Gx, Gy

        # print("X:{:.2f}  Y:{:.2f}  Z:{:.2f}".format(g.Gx, g.Gy, g.Gz))
        utime.sleep_ms(50)
    pass


if __name__ == "__main__":
    main()
