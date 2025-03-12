import asyncio
import time

import machine
from machine import Pin

async def blink(led, period_ms):
    while True:
        led.on()
        await asyncio.sleep_ms(period_ms)
        led.off()
        await asyncio.sleep_ms(period_ms)


async def main(led1, led2):
    asyncio.create_task(blink(led1, 400))
    asyncio.create_task(blink(led2, 700))
    await asyncio.sleep(10)
    print("Main stopping...")

if __name__ == '__main__':
    L1 = Pin(25, Pin.OUT) # Groen
    L2 = Pin(26, Pin.OUT) # Geel

    print(f"Machine frequency {machine.freq()}")
    print(f"Local time {time.localtime()}")
    try:
        asyncio.run(main(L1, L2))
    except KeyboardInterrupt as kbi:
        print("Interrupt by keypress")
    finally:
        print("In the finally")
        L1.value(0)
        L2.value(0)
