#Insert PIR sensor to CN6, signal pin to GPIO16

from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin
import time

pri_pin = Pin(16, Pin.IN)
buzzer = machine.Pin(4, machine.Pin.OUT)

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
tft = TFT(spi, 14, 15, 13)



start_time = time.ticks_ms()


def main():

    buzzer.off()

    tft.initg()
    tft.rgb(True)
    tft.fill(TFT.BLACK)
    tft.text((0, 0), "Pir demo", TFT.WHITE, sysfont, 2, nowrap=True)

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

                tft.text((0, 50), "Welcome", TFT.YELLOW, sysfont, 2, nowrap=True)
                tft.text((0, 70), "Makerfabs", TFT.YELLOW, sysfont, 2, nowrap=True)
                buzzer.on()
                

        else:
            if trigger_flag is 1:
                trigger_flag = 0
                trigger_time = int((time.ticks_ms() - trigger_time) / 1000)
                print("Trigger time:"  + str(trigger_time))

                tft.fillrect((0, 50), (128, 70), TFT.BLACK)
                buzzer.off()
        
        time.sleep(1)
        
        
main()