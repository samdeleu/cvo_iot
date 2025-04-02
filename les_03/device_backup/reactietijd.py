from machine import Pin
import time
import random

led_internal = Pin(2, Pin.OUT)

led_r = Pin(13, Pin.OUT)
led_g = Pin(12, Pin.OUT)
led_b = Pin(14, Pin.OUT)

knop = Pin(16, Pin.IN)

led_actie = Pin(23, Pin.OUT)

def blink(led, aantal_keer = 10):
    for on_off in range(aantal_keer):
        led.value(on_off % 2)
        time.sleep_ms(50)
    led.off()

def check_knop(aantal_keer = 2):
    print(f"Test de drukknop {aantal_keer} maal, interne LED moet aangaan")
    if aantal_keer <= 0:
        aantal_keer = 1
    while aantal_keer > 0:        
        if knop.value() == 1:
            led_internal.on()
            time.sleep(2)
            aantal_keer = aantal_keer -1
            led_internal.off()
        
def start_spel():
    blink(led_r, aantal_keer=3)
    blink(led_g, aantal_keer=3)
    blink(led_b, aantal_keer=3)
    led_b.on()
    led_r.on()
    led_g.on()
    led_actie.on()
    time.sleep(1)
    led_b.off()
    time.sleep(1)
    led_g.off()
    time.sleep(1)
    led_r.off()
    time.sleep(1)
    led_actie.off()
    
blink(led_r)
blink(led_g)
blink(led_b)
blink(led_actie)

check_knop()

while True:
    pauze = random.randint(2, 5)
    print(f"Lampje gaat aan in {pauze} seconden")
    start_spel()
    time.sleep(pauze)
    start = time.ticks_ms()
    stop = 0
    led_actie.on()
    
    skip = 0
    while skip == 0:
        if knop.value() == 1:
            print(f"Knop ingedrukt: {knop.value()}: {start}-{stop}")
            stop = time.ticks_ms()
            skip = 1
            led_r.on()
        elif time.ticks_ms()-start >= 1000:
            skip = -1
        
        if skip == -1:
            led_b.on()
        else:
            diff = time.ticks_diff(stop, start)
            print(f"XXXXX {diff} xxxxx")
            if diff <= 100:
                led_r.on()
            elif diff > 100 and diff <= 200:
                led_g.on()
            elif diff > 200 and diff <= 500:
                led_b.on()
                led_g.on()
            else:
                led_b.on()
            
        