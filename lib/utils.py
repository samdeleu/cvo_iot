import time

def blink(led, blinks=5):
    start = led.value()
    for i in range(2 * blinks):
        led.value(not led.value())
        time.sleep_ms(200)
    led.value(start)

def test_blink(state=1, nbr=10):
    from machine import Pin
    l = Pin(15, Pin.OUT)
    l.value(state)
    blink(l, nbr)


if __name__ == "__main__":
    
    print("---testing--------")
    test_blink(0, 10)
