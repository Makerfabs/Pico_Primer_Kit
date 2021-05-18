import utime
from servo import Servo

s1 = Servo(16)       # initialize servo on GPIO pin 0

while True:
    s1.goto(100)      # move arm all the way to one side
    utime.sleep(1)
    s1.goto(800)   # move arm all the way to the other side
    utime.sleep(1)
    