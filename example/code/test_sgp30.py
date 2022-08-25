from machine import SPI, Pin, I2C
import time
from sgp30 import SGP30

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400_000)
sensor = SGP30(i2c)

def main():

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
        # The IAQ measurement must be triggered exactly once per second (SGP30)
        # to get accurate values.
        time.sleep(1)


main()
