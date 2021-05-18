from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin
import utime
import math
from servo import Servo


spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
# def __init__( self, spi, aDC, aReset, aCS) :
tft = TFT(spi, 14, 15, 13)

s1 = Servo(16)
relay = Pin(26, Pin.OUT)

button_1 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
button_2 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
button_3 = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)


def main():
    tft.initg()
    tft.rgb(True)
    tft.fill(TFT.BLACK)
    tft.text((10, 10), "Servo Control", TFT.WHITE, sysfont, 1, nowrap=True)

    tft.text((0, 40), "BUTTON_1 => Servo 0",
             TFT.WHITE, sysfont, 1, nowrap=True)
    tft.text((0, 60), "BUTTON_2 => Servo 90",
             TFT.WHITE, sysfont, 1, nowrap=True)
    tft.text((0, 80), "BUTTON_3 => Relay", TFT.WHITE, sysfont, 1, nowrap=True)

    relay.value(0)

    while True:
        if button_1.value() == 0:
            s1.goto(100)

        if button_2.value() == 0:
            s1.goto(800)

        if button_3.value() == 0:
            relay.toggle()
            utime.sleep_ms(500)


if __name__ == "__main__":
    main()
