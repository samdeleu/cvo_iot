from machine import Pin
import sys
import ubinascii
import json
from lib import simpleWifi_v2
import time

ESP_NAME = "esp_sam"
wifi = simpleWifi_v2.Wifi()
wifi.open()
if wifi.get_status() <= 0:
    print("probleem wifi")
    sys.exit()

MAC = wifi.net.config('mac')
MAC = ubinascii.hexlify(MAC).decode()
print(f"MAC adres:{MAC}")
    