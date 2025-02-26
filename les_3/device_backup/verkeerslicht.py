from machine import TouchPad, Pin
import time

# Definieren van de geconnecteerde pinnen
led_internal = Pin(2, Pin.OUT)

# Definieren van een touch pin
touch0_gpio04 = TouchPad(Pin(4, mode=Pin.IN))

licht_1_red = Pin(23, Pin.OUT)
licht_1_yellow = Pin(22, Pin.OUT)
licht_1_green = Pin(21, Pin.OUT)

licht_2_red = Pin(25, Pin.OUT)
licht_2_yellow = Pin(33, Pin.OUT)
licht_2_green = Pin(32, Pin.OUT)

def licht_1_init(value=1):
    licht_1_red.value(value)
    licht_1_yellow.value(value)
    licht_1_green.value(value)
# Initialize all leds
def licht_2_init(value=1):
    licht_2_red.value(value)
    licht_2_yellow.value(value)
    licht_2_green.value(value)

def start_sequentie(aantal=5):
    for i in range(aantal):
        licht_1_init(1)
        licht_2_init(1)
        time.sleep(0.2)
        licht_1_init(0)
        licht_2_init(0)
        time.sleep(0.2)

# Gewenste toestanden
status = [
    [1, 1, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1, 0, 0],
    [2, 0, 0, 1, 1, 0, 0],
    [2, 1, 0, 0, 1, 0, 0],
    [1, 1, 0, 0, 0, 1, 0],
    [2, 1, 0, 0, 0, 0, 1],
]

start_sequentie()

while True:
    for s in status:
        touch_value = touch0_gpio04.read()
        print(f"Touch value: {touch_value}")
        if touch_value <= 250:
            start_sequentie()
         
        licht_1_red.value(s[1])
        licht_1_yellow.value(s[2])
        licht_1_green.value(s[3])
        licht_2_red.value(s[4])
        licht_2_yellow.value(s[5])
        licht_2_green.value(s[6])
        
        time.sleep(s[0])
        
