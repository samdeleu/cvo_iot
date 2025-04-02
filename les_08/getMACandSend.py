from simpleWifi_v2 import Wifi
import sys
import ubinascii

wifi = Wifi()
wifi.open()
if wifi.get_status() <= 0:
    print("probleem wifi")
    sys.exit()

MAC = wifi.net.config('mac')
MAC = ubinascii.hexlify(MAC).decode()
print(f"MAC adres:{MAC}")


    