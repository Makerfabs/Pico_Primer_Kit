# Only For Pico W
# Instead of Project 4

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

def decode_weather_request(payload_str):
    json_str = payload_str.replace('\n','').replace('\r','')
    json_result = []

    try:
        json_result = json.loads(json_str)
    except:
        print("Json decode error")

    return json_result
    


def test_main():
    tft.fill(TFT.BLACK)
    tft.text((0, 0), "WiFi Test", TFT.WHITE, sysfont, 2, nowrap=True)

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

        res = urequests.get(url="http://api.openweathermap.org/data/2.5/weather?q=shenzhen&appid=fc55ebaf691fd562af69a4924907c627")
        res_str = res.text
        print(res_str)

        # res_str = """{"coord":{"lon":116.3972,"lat":39.9075},"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}],"base":"stations","main":{"temp":299.09,"feels_like":298.55,"temp_min":299.09,"temp_max":299.09,"pressure":1010,"humidity":31,"sea_level":1010,"grnd_level":1004},"visibility":10000,"wind":{"speed":5.12,"deg":341,"gust":7.61},"clouds":{"all":32},"dt":1661391797,"sys":{"type":1,"id":9609,"country":"CN","sunrise":1661376921,"sunset":1661425102},"timezone":28800,"id":1816670,"name":"Beijing","cod":200}"""

        json_result = decode_weather_request(res_str)
        if json_result == []:
            tft.text((0, 40), "Decode ERR", TFT.WHITE, sysfont, 2, nowrap=True)
            tft.text((0, 60), "TRY AGAIN", TFT.WHITE, sysfont, 2, nowrap=True)
            return
        print(json_result)
        city = json_result["name"]
        weather = json_result["weather"][0]["main"]
        temperature = float(int((json_result["main"]["temp"] - 273.15) * 10) / 10)

        print(city)
        print(weather)
        print(temperature)

        tft.text((0, 40), city, TFT.YELLOW, sysfont, 2, nowrap=True)
        tft.text((0, 60), weather, TFT.BLUE, sysfont, 2, nowrap=True)
        tft.text((0, 80), str(temperature) + " C", TFT.WHITE, sysfont, 2, nowrap=True)


if __name__ == "__main__":
    test_main()

