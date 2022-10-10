import utime as time
from dht import DHT11
from machine import Pin

while True:
    time.sleep(1)
    pin = Pin(16, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)
    
    sensor.measure()
    t  = sensor.temperature()
    h = sensor.humidity()

    print("Temperature: {}".format(t))
    print("Humidity: {}".format(h))