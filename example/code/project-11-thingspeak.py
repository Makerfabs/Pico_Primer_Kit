# Only For Pico W

from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin
import time
import network
import urequests
import json
 
ssid = 'Makerfabs'
password = '20160704'
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)


spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
# def __init__( self, spi, aDC, aReset, aCS) :
tft = TFT(spi, 14, 15, 13)

tft.initg()
tft.rgb(True)

def get_request_thingspeak():
    url_str = "https://api.thingspeak.com/update?"
    api_key = "api_key=KCAT79TTH52MG7EA"
    param = "&field1=300&field2=100"

    urequests.get(url=url_str + api_key + param)
 

def test_main():
    tft.fill(TFT.BLACK)
    tft.text((0, 0), "ThingSpeak Test", TFT.WHITE, sysfont, 2, nowrap=True)

    wlan.connect(ssid, password)
    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )
        temp = str('ip = ' + status[0] )
        tft.text((0, 20), temp, TFT.WHITE, sysfont, 1, nowrap=True)

        # urequests.get(url="https://api.thingspeak.com/update?api_key=KCAT79TTH52MG7EA&field1=100&field2=200")
        get_request_thingspeak()
        tft.text((0, 40), "Send Over", TFT.WHITE, sysfont, 1, nowrap=True)


if __name__ == "__main__":
    test_main()

