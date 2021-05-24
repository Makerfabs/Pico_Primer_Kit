#
#
#
# OLD VERSION DON'T USE !!!!!!!!!!!!!
#
#
# The distance is captured by a Sharpir sensor and displayed on the screen
# Insert SharpIR to CN5
import utime
from dht import DHT11, InvalidChecksum
import os
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin, ADC

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
# def __init__( self, spi, aDC, aReset, aCS) :
tft = TFT(spi, 14, 15, 13)

adc = ADC(machine.Pin(26))

adc_value = 0.0
adc_v = 0.0


def senser():
    value_list = []
    for i in range(10):
        adc_value = adc.read_u16()
        adc_v = adc_value / 65536 * 3.3
        distance = (1.0 / (adc_v / 13.15)) - 0.35
        distance *= 2.54
        value_list.append(distance)
    value_list.sort()

    print(value_list)

    del value_list[9]
    del value_list[0]

    total = 0.0
    for v in value_list:
        total += v
    average = total / 8
    print("DIS:" + str(average) + " cm")
    return average


def main():
    tft.initg()
    tft.rgb(True)
    tft.fill(TFT.BLACK)
    tft.text((10, 10), "IR Distance", TFT.WHITE, sysfont, 1, nowrap=True)

    sensor = DHT11(Pin(16, Pin.OUT, Pin.PULL_DOWN))

    while True:
        utime.sleep(1)

        tft.fillrect((0, 40), (128, 128), TFT.BLACK)
        tft.text((0, 40), "Distance:{}".format(senser()), TFT.YELLOW, sysfont, 2, nowrap=True)


if __name__ == "__main__":
    main()
