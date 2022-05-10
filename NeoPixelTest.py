import machine
from machine import Pin
from machine import Timer
import utime
import urandom
import array
import rp2
from rp2 import PIO, StateMachine, asm_pio


NUM_LEDS = 2
                   
@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1)   .side(0)[T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")  .side(1)    [T2 - 1]
    label("do_zero")
    nop()   .side(0)    [T2 - 1]

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(18))
sm.active(1)
                
def AutoChangeColor():         
    print("blue")
    for j in range(0, 255):
        for i in range(NUM_LEDS):
            ar[i] = j
        sm.put(ar,8)
        utime.sleep_ms(10)
    
    print("red") 
    for j in range(0, 255):
        for i in range(NUM_LEDS):
            ar[i] = j<<8
        sm.put(ar,8)
        utime.sleep_ms(10)

    print("green")
    for j in range(0, 255):
        for i in range(NUM_LEDS):
            ar[i] = j<<16
        sm.put(ar,8)
        utime.sleep_ms(10)
  
    print("white")
    for j in range(0, 255):
        for i in range(NUM_LEDS):
            ar[i] = (j<<16) + (j<<8) + j
        sm.put(ar,8)
        utime.sleep_ms(10)
        
    print("yellow")
    for j in range(0, 255):
        for i in range(NUM_LEDS):
            ar[i] = (j<<16) + (j<<8)# + j
        sm.put(ar,8)
        utime.sleep_ms(10)
        
    print("light blue")
    for j in range(0, 255):
        for i in range(NUM_LEDS):
            ar[i] = (j<<16) + j
        sm.put(ar,8)
        utime.sleep_ms(10)
        
    print("lila")
    for j in range(0, 255):
        for i in range(NUM_LEDS):
            ar[i] = (j<<8) + j
        sm.put(ar,8)
        utime.sleep_ms(10)
        
    nop()
  
while (True):
    AutoChangeColor()
"""  
"""
