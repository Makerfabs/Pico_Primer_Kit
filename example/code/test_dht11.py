import utime
import rp2
from rp2 import PIO, asm_pio
from machine import Pin

from dht import DHT11

# main program
dht_data = Pin(26, Pin.IN, Pin.PULL_UP)

sm = rp2.StateMachine(1)  # create empty state machine
utime.sleep(2)  # wait for DHT11 to start up

while True:
    print('reading')

    data = []
    total = 0
    sm.init(DHT11, freq=1600000, set_base=dht_data, in_base=dht_data,
            jmp_pin=dht_data)  # start state machine

    # state machine frequency adjusted so that PIO countdown during 'readdata' ends somewhere between the
    # duration of a '0' and a '1' high signal
    sm.active(1)

    for i in range(5):  # data should be 40 bits (5 bytes) long
        print("log3")
        data.append(sm.get())  # read byte

    print("data: " + str(data))

    # check checksum (lowest 8 bits of the sum of the first 4 bytes)
    for i in range(4):
        total = total+data[i]
    if((total & 255) == data[4]):
        humidity = data[0]  # DHT11 provides integer humidity (no decimal part)
        # DHT11 provides signed integer temperature (no decimal part)
        temperature = (1-2*(data[2] >> 7))*(data[2] & 0x7f)
        print("Humidity: %d%%, Temp: %dC" % (humidity, temperature))
    else:
        print("Checksum: failed")
    utime.sleep_ms(500)
