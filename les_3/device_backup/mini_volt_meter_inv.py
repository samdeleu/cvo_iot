from machine import Pin, ADC, SoftI2C, I2C
from ssd1306 import SSD1306_I2C
import time


potmeter = ADC(Pin(26, Pin.IN))
potmeter.atten(ADC.ATTN_11DB)
#potmeter.init(atten=ADC.ATTN_11DB)
i2c_face = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled = SSD1306_I2C(width=128, height=64, i2c=i2c_face, addr=0x3C)

oled.fill(0)
oled.fill_rect(0, 0, 32, 32, 1)
oled.fill_rect(2, 2, 28, 28, 0)
oled.vline(9, 8, 22, 1)
oled.vline(16, 2, 22, 1)
oled.vline(23, 8, 22, 1)
oled.fill_rect(26, 24, 2, 4, 1)
oled.text('MicroPython', 40, 0, 1)
oled.text('SSD1306', 40, 12, 1)
oled.text('OLED 128x64', 40, 24, 1)
oled.show()
time.sleep(4)
oled.fill(0)
oled.show()
                   
while True:
    valmeter = potmeter.read()
#    print(f"Gemeten waarde: {valmeter}-{bin(valmeter)}")
#    print(f"Spanning: {valmeter*3.3/4095}V")
    spanning = round(valmeter*3.3/4095, 3)
    oled.fill_rect(32, 20, 60, 16, 1) 
    oled.text(f"{spanning}V", 40, 24, 0)
    oled.contrast(int(valmeter*255/4095))
    oled.show()
    # s = text
    # x = horizontaal
    # y = vertikaal
    
    time.sleep(0.05)
    oled.fill(0)
