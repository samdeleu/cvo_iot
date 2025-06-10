from machine import Pin
import json
import time
import binascii
import network
import espnow
from lib import utils

ESP_NAME="esp_sam1"

mac_addrs = None

with open("macaddr.json", "r") as f:
    print("XXXXX")
    mac_addrs = json.load(f)

print(mac_addrs)

# led
led = Pin(25, Pin.OUT)


# Network
net = network.WLAN(network.WLAN.IF_STA)
net.active(True)
net.config(channel=1)
net.disconnect()

# ESP32 specifics
espnet = espnow.ESPNow()
espnet.active(True)

mac_addrs_hex = []
for a in mac_addrs:
    x = bytearray.fromhex(a["mac"])
    print("2", a["mac"], x)
    mac_addrs_hex.append(x)
    espnet.add_peer(x)
    
while True:
    t = time.time()
    try:
        for to in mac_addrs_hex:
            print(f"{t}: send to: {to}")
            response = espnet.send(to, f"{t} from: {ESP_NAME}, cmd:LED=on")
            print(f"  response 1: {response}")
            time.sleep(2)
            response = espnet.send(to, f"{t} from: {ESP_NAME}, cmd:LED=off")
            print(f"  response 2: {response}")
    except Exception as e:
        print("ERROR sending: {e}")
    time.sleep(2)

