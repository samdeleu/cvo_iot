from simpleWifi_v2 import Wifi
import socket
import sys
import time

wifi = Wifi()
wifi.open()
if wifi.get_status() < 0:
    print("probleem connectie wifi")
    sys.exit()
print("verbinding met wifi")
wifi.net.config(pm=wifi.net.PM_NONE)  # Power Mnagement van wifi zetten op disable

ch = wifi.net.config("channel")  # Power Mnagement van wifi moduleuitlezen
print(f"Current channel: {ch}")

    