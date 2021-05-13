import utime
from machine import Pin, I2C

buzzer = machine.Pin(4, machine.Pin.OUT)

led_1 = machine.Pin(18, machine.Pin.OUT)
led_2 = machine.Pin(19, machine.Pin.OUT)
led_3 = machine.Pin(20, machine.Pin.OUT)

button_1 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
button_2 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
button_3 = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)

buzzer.value(1)
utime.sleep_ms(500)
buzzer.value(0)

led_1.value(0)
led_2.value(0)
led_3.value(0)

while(True):
    if button_1.value() == 0:
        led_1.toggle()
    if button_2.value() == 0:
        led_2.toggle()
    if button_3.value() == 0:
        led_3.toggle()
    utime.sleep_ms(500)
    
