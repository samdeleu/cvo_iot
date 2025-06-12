from machine import Pin
import time
import json
import network
import espnow
from lib import utils


# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.WLAN.IF_STA)
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

espnet = espnow.ESPNow()
espnet.active(True)

# led
led = Pin(25, Pin.OUT)
led.off()
utils.blink(led, 10)

with open("macaddr.json", "r") as f:
    print("Loading addresses...")
    mac_addrs = json.load(f)


led.off()


macs = []
names = []
mac_addrs_hex = []
for a in mac_addrs:
    macs.append(a["mac"])
    names.append(a["espname"])
    x = bytearray.fromhex(a["mac"])
    print(a["mac"], a["espname"], x)
    mac_addrs_hex.append(x)
    espnet.add_peer(x)


while True:
    print("Start receiving...")
    host, msg = espnet.recv()
    if msg:
        decoded_msg = msg.decode()# msg == None if timeout in recv()
        print(host, msg)
        if "LED=on" in msg:
            led.on()
        if "LED=off" in msg:
            led.off()
        if msg == b'end':
            break