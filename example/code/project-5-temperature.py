import utime
from dht import DHT11, InvalidChecksum
import os
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
# def __init__( self, spi, aDC, aReset, aCS) :
tft = TFT(spi, 14, 15, 13)


def main():
    tft.initg()
    tft.rgb(True)
    tft.fill(TFT.BLACK)
    tft.text((10, 10), "Temperature Display", TFT.WHITE, sysfont, 1, nowrap=True)

    sensor = DHT11(Pin(16, Pin.OUT, Pin.PULL_DOWN))

    while True:
        utime.sleep(1)

        t = (sensor.temperature)
        h = (sensor.humidity)
        print("Temperature: {}".format(t))
        print("Humidity: {}".format(h))

        tft.fillrect((0, 40), (128, 128), TFT.BLACK)
        tft.text((0, 40), "Temp:{} C".format(t), TFT.YELLOW, sysfont, 2, nowrap=True)
        tft.text((0, 80), "Humi:{} %".format(h), TFT.GREEN, sysfont, 2, nowrap=True)


if __name__ == "__main__":
    main()
