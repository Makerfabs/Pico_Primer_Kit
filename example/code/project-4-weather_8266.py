# Connect to WiFi through ESP8266 module and get the weather.
# Insert MaBee 8266 to CN1
# API from "api.openweathermap.org" is not stable, please try more and pay attention to the serial port information.

import os
import utime
import machine
import json
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
# def __init__( self, spi, aDC, aReset, aCS) :
tft = TFT(spi, 14, 15, 13)
uart = machine.UART(0)


def sendCMD_waitRespLine(cmd, timeout=2000):
    print("CMD: " + cmd)
    cmd += "\r\n"
    uart.write(cmd)
    return waitRespLine(timeout)


def waitRespLine(timeout=2000):
    back_str = ""
    prvMills = utime.ticks_ms()
    while (utime.ticks_ms()-prvMills) < timeout:
        if uart.any():
            # print(uart.readline().decode('utf8'))
            temp = uart.readline().decode('utf8')
            print(temp)
            if temp.find(",") != -1:
                back_str = back_str + temp[temp.find(",") + 1:]
    back_str = back_str.replace("\r", "").replace("\n", "").replace(" ", "")
    return back_str


def main():

    tft.initg()
    tft.rgb(True)
    tft.fill(TFT.BLACK)
    tft.text((0, 0), "8266 Weather", TFT.WHITE, sysfont, 1, nowrap=True)
    tft.text((0, 20), "Waiting...", TFT.WHITE, sysfont, 1, nowrap=True)

    # print sys info
    print(os.uname())

    # print uart info
    print(uart)

    # Moudle init
    sendCMD_waitRespLine("AT+GMR")
    sendCMD_waitRespLine("ATE0")

    # Connect Wifi
    sendCMD_waitRespLine("AT+CWMODE=1")
    sendCMD_waitRespLine("AT+CWJAP=\"Makerfabs\",\"20160704\"", timeout=10000)

    # Http
    json_str = ""
    json_str = sendCMD_waitRespLine(
        """AT+HTTPCLIENT=2,0,"http://api.openweathermap.org/data/2.5/weather?q=beijing&appid=fc55ebaf691fd562af69a4924907c627",,,1""", timeout=10000)
    print(json_str)
    json_result = []
    try :
        json_result = json.loads(json_str)
    except :
        tft.text((0, 40), "Decode ERR", TFT.WHITE, sysfont, 2, nowrap=True)
        tft.text((0, 60), "TRY AGAIN", TFT.WHITE, sysfont, 2, nowrap=True)
        return
    print(json_result)
    city = json_result["name"]
    weather = json_result["weather"][0]["main"]
    temperature = json_result["main"]["temp"] - 273.15

    print(city)
    print(weather)
    print(temperature)

    tft.text((0, 40), city, TFT.WHITE, sysfont, 2, nowrap=True)
    tft.text((0, 60), weather, TFT.WHITE, sysfont, 2, nowrap=True)
    tft.text((0, 80), str(temperature), TFT.WHITE, sysfont, 2, nowrap=True)

    print("Over")


if __name__ == "__main__":
    main()
