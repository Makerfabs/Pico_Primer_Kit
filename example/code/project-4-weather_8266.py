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
    # waitRespLine_byte(timeout)
    return waitRespLine_safe(timeout)


def waitRespLine_byte(timeout=2000):
    back_str = ""
    prvMills = utime.ticks_ms()
    while (utime.ticks_ms()-prvMills) < timeout:
        if uart.any():
            # print(uart.readline().decode('utf8'))
            print(uart.readline())


def waitRespLine_safe(timeout=2000):
    prvMills = utime.ticks_ms()
    back_str = ""
    while (utime.ticks_ms()-prvMills) < timeout:
        if uart.any():
            temp_str = ""
            try:
                temp_str = uart.readline().decode('utf8')
            except UnicodeError:
                continue
            else:
                back_str = back_str + temp_str
    # back_str = back_str.replace("\r", "").replace("\n", "").replace(" ", "")
    print(back_str)
    return back_str


def decode_weather_request(payload_str):
    payload_list = payload_str.split('\n')
    # print(payload_list)

    json_str = ""
    for line in payload_list:
        if line == "":
            continue
        elif line == "OK":
            continue
        else:
            if line.find("+HTTPCLIENT:") != -1:
                split_location = line.find(",")
                json_str += line[split_location + 1:]

    # print(json_str)

    json_result = []
    try:
        json_result = json.loads(json_str)
    except:
        print("Json decode error")
    # print(json_result)
    return json_result


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

    # request weather
    # sendCMD_waitRespLine(
    #      """AT+HTTPCLIENT=2,0,"http://api.openweathermap.org/data/2.5/weather?q=beijing&appid=fc55ebaf691fd562af69a4924907c627",,,1""", timeout=10000)

    # # Http
    json_str = ""
    json_str = sendCMD_waitRespLine(
        """AT+HTTPCLIENT=2,0,"http://api.openweathermap.org/data/2.5/weather?q=beijing&appid=fc55ebaf691fd562af69a4924907c627",,,1""", timeout=10000)
    # print(json_str)
    json_result = decode_weather_request(json_str)
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

    print("Over")


if __name__ == "__main__":
    main()
