# The voltage value of the read slide potentimeter is displayed on the screen
# Insert MaBee Slide Potentimeter to CN5

import machine
import utime
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin, ADC
import math

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
# def __init__( self, spi, aDC, aReset, aCS) :
tft = TFT(spi, 14, 15, 13)

adc = ADC(machine.Pin(26))


def main():
    tft.initg()
    tft.rgb(True)
    tft.fill(TFT.BLACK)
    tft.text((0, 0), "Display_ADC", TFT.WHITE, sysfont, 1, nowrap=True)
    tft.text((10, 70), "0V", TFT.WHITE, sysfont, 1, nowrap=True)
    tft.text((100, 70), "3.3V", TFT.WHITE, sysfont, 1, nowrap=True)

    while True:
        adc_value = adc_read()
        tft.fillrect((10, 50), (128, 10), TFT.BLACK)
        tft.fillrect((10, 50), ((int)(100 * (adc_value / 3.3)), 10), TFT.RED)
        tft.text((0, 15), "Volt:{:.2f} V".format(
            adc_value), TFT.WHITE, sysfont, 1, nowrap=True)
        utime.sleep_ms(500)


def adc_read():
    adc_value = 0.0
    adc_v = 0.0
    value_list = []
    for i in range(10):
        adc_value = adc.read_u16()
        adc_v = adc_value / 65536 * 3.3
        value_list.append(adc_v)
    value_list.sort()

    del value_list[9]
    del value_list[0]

    total = 0.0
    for v in value_list:
        total += v
    average = total / 8
    print("Volt:" + str(average) + " V")
    return average


if __name__ == "__main__":
    main()
