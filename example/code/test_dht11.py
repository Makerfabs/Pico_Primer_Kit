import utime as time
from dht import DHT11, InvalidChecksum
from machine import Pin

while True:
    time.sleep(1)
    pin = Pin(16, Pin.OUT, Pin.PULL_DOWN)
    sensor = DHT11(pin)
    t  = (sensor.temperature)
    #time.sleep_ms(2000)
    h = (sensor.humidity)
    #time.sleep_ms(2000)
    print("Temperature: {}".format(sensor.temperature))
    print("Humidity: {}".format(sensor.humidity))