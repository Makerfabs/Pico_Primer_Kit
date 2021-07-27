# Control onboard leds via buttons
# And display status on TFT screen
# Don't need any module

from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin
import time
import math
import array
from rp2 import PIO, StateMachine, asm_pio

# Configure the number of WS2812 LEDs.
NUM_LEDS = 10
@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1) .side(0) [T3 - 1]
    jmp(not_x, "do_zero") .side(1) [T1 - 1]
    jmp("bitloop") .side(1) [T2 - 1]
    label("do_zero")
    nop() .side(0) [T2 - 1]
# Create the StateMachine with the ws2812 program, outputting on Pin(22).
sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(16))
# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)


spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
# def __init__( self, spi, aDC, aReset, aCS) :
tft = TFT(spi, 14, 15, 13)


def main():
    tft.initg()
    tft.rgb(True)
    tft.fill(TFT.BLACK)
    tft.text((0, 0), "WS2812 Show", TFT.WHITE, sysfont, 2, nowrap=True)
    
    while True:
        ar = array.array("I", [0 for _ in range(NUM_LEDS)])
        tft.fillrect((0, 40), (128, 128), TFT.BLACK)
        tft.text((30, 60), "BLUE", TFT.BLUE, sysfont, 4, nowrap=True)
        print("blue")

        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = j
                sm.put(ar,8)
            time.sleep_ms(5)

        tft.fillrect((0, 40), (128, 128), TFT.BLACK)
        tft.text((40, 60), "RED", TFT.RED, sysfont, 4, nowrap=True)
        print("RED")

        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = j<<8
                sm.put(ar,8)
            time.sleep_ms(5)

        tft.fillrect((0, 40), (128, 128), TFT.BLACK)
        tft.text((20, 60), "GREEN", TFT.GREEN, sysfont, 4, nowrap=True)
        print("GREEN")
        for j in range(0, 255):
            for i in range(NUM_LEDS):
                ar[i] = j<<16
                sm.put(ar,8)
            time.sleep_ms(5)


if __name__ == "__main__":
    main()
