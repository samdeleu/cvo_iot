import sys
import ubinascii
import json
from lib import simpleWifi_v2
from lib.connectMQTT import mqtt_connect_public_hivemq
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

mqtt = None
mqtt = mqtt_connect_public_hivemq()
if mqtt is None:
    print("mqtt fail")
    wifi.close()
    sys.exit()

payload = json.dumps({"espname": ESP_NAME, "mac": MAC}).encode()
print(payload)
for i in range(3000):
    print("Sending...")
    mqtt.publish("data/cvo/mac", payload)
    time.sleep(5)

    