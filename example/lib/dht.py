import utime
import rp2 
from rp2 import PIO, asm_pio
from machine import Pin

@asm_pio(set_init=(PIO.OUT_HIGH),autopush=True, push_thresh=8) #output one byte at a time
def DHT11():
    #drive output low for at least 20ms
    set(pindirs,1)              #set pin to output  
    set(pins,0)                 #set pin low
    set(y,31)                   #prepare countdown, y*x*100cycles
    label ('waity')
    set(x,31) 
    label ('waitx')
    nop() [25] 
    nop() [25]
    nop() [25]
    nop() [25]                  #wait 100cycles
    jmp(x_dec,'waitx')          #decrement x reg every 100 cycles
    jmp(y_dec,'waity')          #decrement y reg every time x reaches zero
     
    #begin reading from device
    set(pindirs,0)              #set pin to input 
    wait(1,pin,0)               #check pin is high before starting
    wait(0,pin,0)
    wait(1,pin,0)
    wait(0,pin,0)               #wait for start of data

    #read databit
    label('readdata')
    set(x,20)                   #reset x register to count down from 20
    wait(1,pin,0)               #wait for high signal
    label('countdown')
    jmp(pin,'continue')         #if pin still high continue counting
    #pin is low before countdown is complete - bit '0' detected
    set(y,0)                 
    in_(y, 1)                   #shift '0' into the isr
    jmp('readdata')             #read the next bit
        
    label('continue')
    jmp(x_dec,'countdown')      #decrement x reg and continue counting if x!=0
    #pin is still high after countdown complete - bit '1' detected 
    set(y,1)                  
    in_(y, 1)                   #shift one bit into the isr
    wait(0,pin,0)               #wait for low signal (next bit) 
    jmp('readdata')             #read the next bit
    
