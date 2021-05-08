import os
import utime
import machine

def sendAT(uart, str):
    str += "\r\n"
    uart.write(str)
    utime.sleep(3)
    while uart.any():
        print(uart.readline())
    utime.sleep(3)
    while uart.any():
        print(uart.readline())
        
def sendCMD_waitRespLine(cmd, timeout=2000):
    print("CMD: " + cmd)
    cmd += "\r\n"
    uart.write(cmd)
    waitRespLine(timeout)
    print()
    
def waitRespLine(timeout=2000):
    prvMills = utime.ticks_ms()
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            print(uart.readline().decode('utf8'))
            #print(uart.readline())

#print sys info
print(os.uname())

#print uart info
uart = machine.UART(0)
print(uart)
# uart.write("AT+RST\r\n")
# utime.sleep(3)

#Moudle init

sendCMD_waitRespLine("AT+GMR")
sendCMD_waitRespLine("ATE0")

# Connect Wifi
sendCMD_waitRespLine("AT+CWMODE=1")
sendCMD_waitRespLine("AT+CWJAP=\"Makerfabs\",\"20160704\"" ,timeout = 10000)

# sendCMD_waitRespLine("AT+CIFSR")
# sendCMD_waitRespLine("AT+PING=\"free-api.heweather.net\"",timeout = 10000)

# NTP time
# sendCMD_waitRespLine("AT+CIPSNTPCFG?")
# sendCMD_waitRespLine("AT+CIPSNTPCFG=1,8,\"cn.ntp.org.cn\",\"ntp.sjtu.edu.cn\",\"us.pool.ntp.org\"", timeout = 10000)
# sendCMD_waitRespLine("AT+CIPSNTPTIME?")

# TCP
# sendCMD_waitRespLine("AT+CIPMUX=0",timeout = 10000)
# sendCMD_waitRespLine("AT+CIPSTART=\"TCP\",\"free-api.heweather.net\",8080",timeout = 10000)
# sendCMD_waitRespLine("AT+CIPMODE=1",timeout = 10000)
# sendCMD_waitRespLine("AT+CIPSEND",timeout = 10000)
# 
# sendCMD_waitRespLine("GET /s6/weather/now?location=Newyork&key=2d63e6d9a95c4e8f8d3f65d0b5bcdf7f&lang=en\r\n",timeout = 10000)
# 
# sendCMD_waitRespLine("+++",timeout = 10000)

# Http

sendCMD_waitRespLine("""AT+HTTPCLIENT=2,0,"http://api.openweathermap.org/data/2.5/weather?q=beijing&appid=fc55ebaf691fd562af69a4924907c627",,,1""",timeout = 10000)
# sendCMD_waitRespLine("AT+HTTPCLIENT=2,0,\"https://free-api.heweather.net/s6/weather/now?location=Newyork&key=2d63e6d9a95c4e8f8d3f65d0b5bcdf7f&lang=en\",1",10000)
#https://free-api.heweather.net/s6/weather/now?location=Newyork&key=2d63e6d9a95c4e8f8d3f65d0b5bcdf7f&lang=en

#anxinke example

# sendCMD_waitRespLine("AT+HTTPCLIENT=3,0,\"http://httpbin.org/post\",\"httpbin.org\",\"/post\",1,\"field1=value1&field2=value2\"",timeout = 10000)

print()
print("Over")

