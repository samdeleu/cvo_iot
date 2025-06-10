import asyncio

async def taak1():
    while True:
        print("Taak 1 is bezig")
        await asyncio.sleep(1)
        
async def taak2():
    while True:
        print("Taak 2 is bezig")
        await asyncio.sleep(3)
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(taak1())
    loop.create_task(taak2())
    loop.run_forever()
