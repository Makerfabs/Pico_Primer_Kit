import machine
import time

adc = machine.ADC(machine.Pin(26))

adc_value = 0.0
adc_v = 0.0

def senser():
    value_list = []
    for i in range(10):
        adc_value = adc.read_u16()
        adc_v =  adc_value / 65536 * 3.3
        distance = (1.0 / (adc_v / 13.15)) - 0.35
        distance *= 2.54
        value_list.append(distance)
    value_list.sort()
     
    print(value_list)
     
    del value_list[9]
    del value_list[0]
     
    total = 0.0
    for v in value_list:
        total += v
    average = total / 8
    print("DIS:" + str(average) + " cm")
    
    
    


while True:
    senser()
    time.sleep_ms(500)