from machine import Pin
import asyncio
import json
import time
import binascii
import network
import espnow
import sys
import socket
from lib import utils
from lib.simpleWifi_v2 import Wifi

wifi = Wifi()
wifi.open()
if wifi.get_status() < 0:
    print("Probleem met de wifi")
    sys.exit()

print("Verbonden met de Wifi")
SERVER = "192.168.0.192"
ESP_NAME="esp_sam1"
CNT = 0
TIMES_TO_SEND = 2

mac_addrs = None
with open("macaddr.json", "r") as f:
    mac_addrs = json.load(f)
print("Peer MAC Addresses configured on device\n", mac_addrs)

macs = []
names = []
for a in mac_addrs:
    macs.append(a["mac"])
    names.append(a["espname"])
mac2name = dict(zip(macs, names))
print(mac2name)

# led
led_send = Pin(15, Pin.OUT)
led_recv = Pin(25, Pin.OUT)
utils.blink(led_send)
utils.blink(led_recv)

# Network activation only
net = network.WLAN(network.WLAN.IF_STA)
net.active(True)
net.disconnect()

# ESP32 specifics: reciever
espnet_recv = espnow.ESPNow()
espnet_recv.active(True)

mac_addrs_hex = []
for a in mac_addrs:
    x = bytearray.fromhex(a["mac"])
    print("2", a["mac"], x)
    mac_addrs_hex.append(x)
    espnet_send.add_peer(x)

async def send(times):
    global CNT
    print("Start van zender")
    while True:
        for i in range(times):
            espnet_send.send(f"id:{CNT},msg:TEST")
            print(f"boodschap met id:{CNT} verzonden")
        CNT = CNT+1
        await asyncio.sleep(2)

async def recv():
    host = None
    msg = None
    host, msg = espnet_recv.recv(50)  # esp receiver waits 50ms before timing out
    return host, msg


async def getmsg(tblmac2name):
    print("start ontvanger")
    num_lines = 0
    while True:
        host,msg = await recv()
        print(f"Received from {host}: {msg}")
        if msg and host:
            host = binascii.hexlify(host).decode()
            print("Ontvangen boodschap:", msg.decode(), " van:", tblmac2name[host])
            if num_lines < 100:
                print(f"......................... {num_lines} .........................")
            if num_lines == 100:
                print("###################### 100 ##################################")
            num_lines = num_lines + 1
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(send(TIMES_TO_SEND))
    loop.create_task(getmsg(mac2name))
    loop.run_forever()
