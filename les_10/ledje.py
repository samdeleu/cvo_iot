import time
from machine import Pin

# led
led = Pin(25, Pin.OUT)
led.on()
time.sleep(2)
led.off()

led2 = Pin(15, Pin.OUT)
led2.on()
time.sleep(2)
led2.off()