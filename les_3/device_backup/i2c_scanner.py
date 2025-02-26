from machine import SoftI2C as I2C, Pin

i2c = I2C(scl=Pin(22), sda=Pin(21))
devices = i2c.scan()

if len(devices) == 0:
    print("Geen devices gevonden")
    
else:
    print("Er zijn devices")
    for d in devices:
        print(f"address: {hex(d)}")


        

          