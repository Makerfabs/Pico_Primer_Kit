from machine import Pin
import time

pri_pin = Pin(16, Pin.IN, Pin.PULL_DOWN)

start_time = time.ticks_ms()

def main2():
    while True:
        status = pri_pin.value()
        print("Status:" + str(status))
        time.sleep(0.5)

def main():
    trigger_flag = 0
    trigger_time = 0
    while True:
        status = pri_pin.value()
        print("Runtime:" + str(int((time.ticks_ms() - start_time) / 1000)))
        print("Status:" + str(status))
        
        if status is 1:
            if trigger_flag is 0:
                trigger_flag = 1
                trigger_time = time.ticks_ms()

        else:
            if trigger_flag is 1:
                trigger_flag = 0
                trigger_time = int((time.ticks_ms() - trigger_time) / 1000)
                print("Trigger time:"  + str(trigger_time))
        
        time.sleep(1)
        
        
main()