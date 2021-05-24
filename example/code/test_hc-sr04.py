# code from :https://github.com/callysophie/pico-parking-sensor/blob/main/ultrasonicsensor.py
from machine import Pin
import utime

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

# creates a loop to run the ultra function ten times a second


while True:
    ultra()
    utime.sleep(0.5)

