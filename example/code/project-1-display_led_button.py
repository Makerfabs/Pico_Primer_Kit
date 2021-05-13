# Control onboard leds via buttons
# And display status on TFT screen
# Don't need any module

from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin
import utime
import math


spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
# def __init__( self, spi, aDC, aReset, aCS) :
tft = TFT(spi, 14, 15, 13)

buzzer = machine.Pin(4, machine.Pin.OUT)

led_1 = machine.Pin(18, machine.Pin.OUT)
led_2 = machine.Pin(19, machine.Pin.OUT)
led_3 = machine.Pin(20, machine.Pin.OUT)

button_1 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
button_2 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
button_3 = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)

param_list = ["Button1", "Button2", "Button3", "LED1", "LED2", "LED3"]
state_list = [0, 0, 0, 1, 1, 1]
flag = 1


def main():
    tft.initg()
    tft.rgb(True)
    tft.fill(TFT.BLACK)
    tft.text((0, 0), "Display_led_button", TFT.WHITE, sysfont, 1, nowrap=True)
    for i in range(6):
        tft.text((0, i * 15 + 15),
                 param_list[i], TFT.WHITE, sysfont, 1, nowrap=True)

    display_state()
    while True:
        if read_button() == 1:
            display_state()
            utime.sleep_ms(500)

# Screen display and control leds
def display_state():

    tft.fillrect((60, 15), (128, 128), TFT.BLACK)

    led_1.value(state_list[0])
    led_2.value(state_list[1])
    led_3.value(state_list[2])

    for i in range(6):
        if state_list[i] == 0:
            tft.text((60, i * 15 + 15), "OFF",
                     TFT.WHITE, sysfont, 1, nowrap=True)
        else:
            tft.text((60, i * 15 + 15), "ON", TFT.RED, sysfont, 1, nowrap=True)

# Read button values and return wether button pushed
def read_button():
    if button_1.value() == 0:
        state_list[0] = not state_list[0]
        state_list[3] = not state_list[3]
        return 1

    if button_2.value() == 0:
        state_list[1] = not state_list[1]
        state_list[4] = not state_list[4]
        return 1

    if button_3.value() == 0:
        state_list[2] = not state_list[2]
        state_list[5] = not state_list[5]
        return 1
    return 0


if __name__ == "__main__":
    main()
