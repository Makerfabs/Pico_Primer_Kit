# The distance is captured by a Sharpir sensor and displayed on the screen
# Insert HC-SR04 to CN6
import utime
import os
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
# def __init__( self, spi, aDC, aReset, aCS) :
tft = TFT(spi, 14, 15, 13)
trigger = Pin(16, Pin.OUT)
echo = Pin(17, Pin.IN)

# creates a function
def ultra():
    print("start")
    # turns off trigger, then waits 2 microseconds
    trigger.low()
    utime.sleep_us(2)
    # turns on trigger for 5 microseconds
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    # creates a loop that checks the echo pin - if nothing is received, updates a variable called signaloff
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    # creates another loop that checks echo pin - if something is received, updates a variable called signalon
    while echo.value() == 1:
        signalon = utime.ticks_us()
    # creates a variable called timepassed which stores the value of the time for the pulse to return as an echo
    timepassed = signalon - signaloff
    # creates a variable called distance to store value of timepassed as a distance in centimetres
    distance = (timepassed * 0.0343) / 2

    # prints distance in console
    print("The distance from object is ", distance, "cm")
    return distance


def main():
    tft.initg()
    tft.rgb(True)
    tft.fill(TFT.BLACK)
    tft.text((10, 10), "Ultra Distance", TFT.WHITE, sysfont, 1, nowrap=True)
    tft.text((0, 30), "Distance:", TFT.YELLOW, sysfont, 2, nowrap=True)

    while True:
        utime.sleep(0.3)

        tft.fillrect((0, 50), (128, 128), TFT.BLACK)
        tft.text((0, 50), "{} cm".format(ultra()), TFT.YELLOW, sysfont, 2, nowrap=True)


if __name__ == "__main__":
    main()
