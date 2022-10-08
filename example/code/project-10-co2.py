# Simple SGP30 message display
# Insert SGP30 to CN3, sda to GPIO8, scl to GPIO9

from machine import SPI, Pin, I2C
from ST7735 import TFT
from sysfont import sysfont
import time
from sgp30 import SGP30
import sht31
import network
import socket
import _thread

ssid = 'Makerfabs'
password = '20160704'

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W + Mabee CO2</title></head>
    <body> <h1>Pico W + Mabee CO2</h1>
        <p>%s</p>
        <p>%s</p>
        <p>%s</p>
        <p>%s</p>
    </body>
</html>
"""

tvoc_str = ""
eco2_str = ""
temp_str = ""
humi_str = ""

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
tft = TFT(spi, 14, 15, 13)
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400_000)
sensor = SGP30(i2c)
sensor2 = sht31.SHT31(i2c, addr=0x44)
wlan = network.WLAN(network.STA_IF)

tft.initg()
tft.rgb(True)

def main():

    ip_str = wifi_connect()

    tft.fill(TFT.BLACK)
    tft.text((0, 0), "SGP30 demo", TFT.WHITE, sysfont, 2, nowrap=True)
    tft.text((0, 20), ip_str, TFT.WHITE, sysfont, 1, nowrap=True)

    sensor_init()
    _thread.start_new_thread(sensor_task,())

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on', addr)

    while True:
        try:
            cl, addr = s.accept()
            print('client connected from', addr)
            request = cl.recv(1024)
            print(request)
            response = html % (tvoc_str,eco2_str,temp_str,humi_str)

            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()

        except OSError as e:
            cl.close()
            print('connection closed')

        

def wifi_connect():
    wlan.active(True)
    wlan.connect(ssid, password)

    ip = "no connect"
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
        ip = str('ip = ' + status[0] )

    return ip

def sensor_init():
    print(i2c.scan())
    
    sensor.sgp30_probe()
    print("SGP sensor probing successful")
    feature_set_version, product_type = sensor.sgp30_get_feature_set_version()
    print("Feature set version: ", feature_set_version)
    print("Product type: ", product_type)
    serial_id = sensor.sgp30_get_serial_id()
    print("SerialID: ", serial_id)

    # Read gas raw signals
    ethanol_raw_signal, h2_raw_signal = sensor.sgp30_measure_raw_blocking_read()
    print("Ethanol raw signal: ", ethanol_raw_signal)
    print("H2 raw signal: ", h2_raw_signal)

    # If no baseline is available or the most recent baseline is more than
    # one week old, it must discarded. A new baseline is found with sgp30_iaq_init
    sensor.sgp30_iaq_init()
    print("sgp30_iaq_init done")

def sensor_task():
    global tvoc_str
    global eco2_str
    global temp_str
    global humi_str

    start = 0
    while True:
        if (time.ticks_ms() - start) > 2000:
            tvoc_ppb, co2_eq_ppm = sensor.sgp30_measure_iaq_blocking_read()
            print("tVOC  Concentration: ", tvoc_ppb, " ppb")
            print("CO2eq Concentration: ", co2_eq_ppm, " ppm")

            temp,humi = sensor2.get_temp_humi()
            print("Temperature:",temp)
            print("Humidity:",humi)

            tvoc_str = "TVOC " + str(tvoc_ppb) + " ppb" 
            eco2_str = "ECO2 " + str(co2_eq_ppm) + " ppm" 
            temp_str = "Temp " + str(temp) + " C"
            humi_str = "Humi " + str(humi) + " %"

            tft.fillrect((0, 40), (128, 40), TFT.BLACK)
            tft.text((0, 40), tvoc_str, TFT.WHITE, sysfont, 1, nowrap=True)
            tft.text((0, 60), eco2_str, TFT.WHITE, sysfont, 1, nowrap=True)
            tft.text((0, 80), temp_str, TFT.WHITE, sysfont, 1, nowrap=True)
            tft.text((0, 100), humi_str, TFT.WHITE, sysfont, 1, nowrap=True)

            start = time.ticks_ms()

        time.sleep(1)


main()
