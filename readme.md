# Pico Primer Kit

```c++
/*
Version:		V1.7
Author:			Vincent
Create Date:	2021/4/16
Note:
	2022/10/11: V1.7 Add project11,12
	2022/10/8: V1.6 Update project10
	2022/9/27: V1.5 Add PicoW support, add new Mabee CO2
	2022/9/20: V1.4 Fix dht11 bug.
	2021/7/27: V1.3 Add WS2812
	2021/5/24: V1.2 Change IR to Ultar distance sensor.
	2021/5/19: V1.1 Add 7 display example with MaBee module.
	
*/
```


![](md_pic/main.jpg)




[toc]

# Makerfabs

[Makerfabs home page](https://www.makerfabs.com/)

[Makerfabs Wiki](https://makerfabs.com/wiki/index.php?title=Main_Page)



# Pico(PicoW) Primer Kit
## Intruduce

### Product Link ：[Raspberry Pi Pico Primer Kit](https://www.makerfabs.com/raspberry-pi-pico-primer-kit.html)

### Wiki Link : 
[Pico_Primer_kit](https://www.makerfabs.com/wiki/index.php?title=Pico_Primer_Kit)

[Pico W_Primer_kit](https://www.makerfabs.com/wiki/index.php?title=Pico_W_Primer_Kit)

Pico Primer Kit is the development shield of Pi Pico. It has ST7735 color screen, 3 LED lights and 3 buttons. There are multiple SPI, I2C, UART, GPIO interfaces.
Kit contains a number of MBEE series modules. Such as potentiometer, DHT11, MPU6050, relay and other modules.

**Now that we have a new kit for Pico W, we have replaced the 8266 module with Mabee CO2.**

Most routines are compatible, the only differences are those related to WiFi.

## Feature

- RP2040 microcontroller chip designed by Raspberry Pi in the United Kingdom
- Dual-core Arm Cortex M0+ processor, the flexible clock running up to 133 MHz
- 264KB of SRAM, and 2MB of onboard Flash memory
- Castellated module allows soldering direct to carrier boards
- USB 1.1 with device and host support
- Low-power sleep and dormant modes
- Drag-and-drop programming using mass storage over USB
- 26 × multi-function GPIO pins
- 2 × SPI, 2 × I2C, 2 × UART, 3 × 12-bit ADC, 16 × controllable PWM channels
- Accurate clock and timer on-chip
- Temperature sensor
- Accelerated floating-point libraries on-chip
- 8 × Programmable I/O (PIO) state machines for custom peripheral support



### Front:

![front](md_pic/front.jpg)

### Back:
![back](md_pic/back.jpg)



# Example
## Equipment list

- Pico Primer Kit
- Pi Pico
- MBee modules

## How To Use?

Attention, all code depends on MicroPython v1.19.1 on 2022-08-19

**Subsequent code may not run due to MicroPython version updates. We provide two firmware.**

- Pico		:	rp2-pico-20220618-v1.19.1.uf2

- PicoW	:	rp2-pico-w-20220819-unstable-v1.19.1-298-gc616721b1.uf2

Because PicoW MicroPython has not been officially released, so the driver of the sensor, subject to the Pico.

 

**If you have any questions，such as how to install the development board, how to download the code.**

**Please refer to :[Get Started with MicroPython on Raspberry Pi Pico](https://hackspace.raspberrypi.org/books/micropython-pico)**



![pin](md_pic/pico_pin.jpg)

## V1.2 Project

### project-1-display_led_button.py

Control onboard leds via buttons.
And display status on TFT screen.
Don't need any module

### project-2-leveling.py

Simple graphic level, read inclination angle with MPU6050.
Insert MaBee MPU6050 to CN3

### project-3-adc_display.py

The voltage value of the read slide potentimeter is displayed on the screen
Insert MaBee Slide Potentimeter to CN5

### project-4-weather_8266.py

Connect to WiFi through ESP8266 module and get the weather.
Insert MaBee 8266 to CN1
API from "api.openweathermap.org" is not stable, please try more and pay attention to the serial port information.

### project-5-temperature .py

The temperature and humidity are obtained through DHT11 and displayed on the screen
Insert MaBee DHT11 to CN6

### ~~project-6-ir_distance.py~~

~~The distance is captured by a Sharpir sensor and displayed on the screen~~
~~Insert SharpIR to CN5~~

### project-6-HC-SR04_distance.py

The distance is captured by a HC-SR04 Ultra sensor and displayed on the screen
Insert SharpIR to CN6

### project-7-servo_control.py

Use button control servo and MaBee relay
Insert Servo to CN6
Insert MaBee Relay to CN5

### project-8-ws2812.py
Insert WS2812 to CN6

### project-9-weather.py

Instead of Project 4 without 8266.

**Only for Pico W**

### project-10-CO2.py

Mabee CO2 message display and run a webserver.

Insert Mabee CO2 to CN3, sda to GPIO8, scl to GPIO9

Need change WiFi config in code.

```python
ssid = 'Makerfabs'
password = '20160704'
```



### project-11-thingspeak.py

A simple example is sending data to ThingSpeak. 

Please replace the Wifi information and Thingspeak interface with the user's own.

**Only for Pico W**

### project-12-PIR_detection.py

PIR induction Demo, when the sensor detects the human body after alarm.

 




## Other test file

All files starting with Test are used by engineers and are not guaranteed to be completely correct. 

But it has some reference value.