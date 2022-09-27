# Simple SGP30 message display
# Insert SGP30 to CN3, sda to GPIO8, scl to GPIO9

from machine import SPI, Pin, I2C
from ST7735 import TFT
from sysfont import sysfont
import time
from sgp30 import SGP30
import sht31

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
tft = TFT(spi, 14, 15, 13)
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400_000)
sensor = SGP30(i2c)
sensor2 = sht31.SHT31(i2c, addr=0x44)


tft.initg()
tft.rgb(True)

def main():

    tft.fill(TFT.BLACK)
    tft.text((0, 0), "SGP30 demo", TFT.WHITE, sysfont, 2, nowrap=True)

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

    # Run periodic IAQ measurements at defined intervals
    while True:
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

        tft.fillrect((0, 20), (128, 40), TFT.BLACK)
        tft.text((0, 20), tvoc_str, TFT.WHITE, sysfont, 1, nowrap=True)
        tft.text((0, 40), eco2_str, TFT.WHITE, sysfont, 1, nowrap=True)
        tft.text((0, 60), temp_str, TFT.WHITE, sysfont, 1, nowrap=True)
        tft.text((0, 80), humi_str, TFT.WHITE, sysfont, 1, nowrap=True)


        time.sleep(1)


main()
