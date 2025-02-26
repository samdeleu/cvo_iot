from machine import Pin, ADC, SoftI2C
from lib.ssd1306 import SSD1306_I2C
import time


led_internal = Pin(2, Pin.OUT)

led_rood = Pin(14, Pin.OUT)
led_groen = Pin(13, Pin.OUT)
led_geel = Pin(15, Pin.OUT)
LEDS = (led_groen, led_rood, led_geel)  # tuple met leds

potmeter = ADC(Pin(26, Pin.IN))
potmeter.atten(ADC.ATTN_11DB)
#potmeter.init(atten=ADC.ATTN_11DB)
i2c_face = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled = SSD1306_I2C(width=128, height=64, i2c=i2c_face, addr=0x3C)


def set_leds(leds, values):
    """set_leds
    param: leds lijst met led objecten
    param: values lijst met gewenste waarde voor elke led
    
    vb: leds uit [0,0,0], aan [1,1,1]
    """
    i=0
    for led in leds:
        led.value(values[i])
        i+=1

def draw_leds(leds, values):
    """set_leds
    param: leds lijst met led objecten
    param: values lijst met gewenste waarde voor elke led
    
    vb: leds uit [0,0,0], aan [1,1,1]
    """
    left_y = 2 #x linker bovenheok blokje
    left_x = 32 #y linker bovenheok blokje
    width = 10 # breedte blokje
    height = 10 # hoogte blokje
    space = 10 # ruimte tussen blokjes
    
    i=0
    for led in leds:
        if values[i] == 1:
            oled.fill_rect(left_x + i * (width + space),
                           left_y, width, height, 1)
        else:
            oled.rect(left_x + i * (width + space),
                      left_y, width, height, 1)
        i+=1

set_leds(LEDS, [0, 0, 0])
time.sleep(0.5)
set_leds(LEDS, [1, 1, 1])
time.sleep(0.5)
set_leds(LEDS, [0, 0, 0])

# oled.invert(1)

while True:
    valmeter = potmeter.read()
    print(f"Gemeten waarde: {valmeter}-{bin(valmeter)}")
    oled.fill(0)
    oled.fill_rect(32, 20, 60, 16, 1) 
    oled.text(f"{valmeter}", 40, 24, 0)
    if valmeter <= 4095//6:
        set_leds(LEDS, [0, 0, 0])
        oled.text("NIETS", 40, 40, 1) 
        draw_leds(LEDS, [0, 0, 0])
    elif valmeter <= 4095//3:
        set_leds(LEDS, [1, 0, 0])
        oled.text("GROEN", 40, 40, 1) 
        draw_leds(LEDS, [1, 0, 0])
    elif valmeter <= 4095//2:
        set_leds(LEDS, [1, 1, 0])
        oled.text("ROOD", 40, 40, 1) 
        draw_leds(LEDS, [1, 1, 0])
    else:
        set_leds(LEDS, [1, 1, 1])
        oled.text("GEEL", 40, 40, 1) 
        draw_leds(LEDS, [1, 1, 1])
    oled.show()
    time.sleep(0.05)
