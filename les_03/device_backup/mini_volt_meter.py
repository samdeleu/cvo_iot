from machine import Pin, ADC, SoftI2C, I2C
from ssd1306 import SSD1306_I2C
import time


potmeter = ADC(Pin(26, Pin.IN))
potmeter.atten(ADC.ATTN_11DB)
#potmeter.init(atten=ADC.ATTN_11DB)
i2c_face = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled = SSD1306_I2C(width=128, height=64, i2c=i2c_face, addr=0x3C)

oled.fill(1)
oled.show()
time.sleep(0.5)
oled.fill(0)
oled.show()
                   
while True:
    valmeter = potmeter.read()
#    print(f"Gemeten waarde: {valmeter}-{bin(valmeter)}")
#    print(f"Spanning: {valmeter*3.3/4095}V")
    spanning = round(valmeter*3.3/4095, 3)
    oled.text(f"{spanning}V", 0, 0)
    oled.hline(0, 8, 128, 1) 
    oled.text(f"{spanning}V", 0, 55)
    oled.hline(0, 52, 128, 1) 
    oled.rect(32, 25, int(spanning*15), 12, 1) 
    oled.vline(60, 20, int(spanning*15), 1) 
    oled.show()
    # s = text
    # x = horizontaal
    # y = vertikaal
    
    time.sleep(0.05)
    oled.fill(0)
