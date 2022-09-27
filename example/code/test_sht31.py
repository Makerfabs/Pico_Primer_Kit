from machine import Pin, I2C
import sht31
import time

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400_000)
sensor = sht31.SHT31(i2c, addr=0x44)



def main():
    while True:
        temp,humi = sensor.get_temp_humi()
        print("Temperature:",temp)
        print("Humidity:",humi)
        time.sleep(1)
        
        
main()