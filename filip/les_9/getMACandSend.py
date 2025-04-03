from simpleWifi_v2 import Wifi
import sys
import ubinascii
from connectMQTT import mqtt_connect_public_hivemq
import time
import json

ESP_NAME = "esp_filiplk"

wifi = Wifi()
wifi.open()
if wifi.get_status() <= 0:
    print("probleem wifi")
    sys.exit()

MAC = wifi.net.config('mac')
MAC = ubinascii.hexlify(MAC).decode()
print(f"MAC adres:{MAC}")

mqtt = None
mqtt = mqtt_connect_public_hivemq()#verbinden met hivemq
if mqtt is None:#geen verbinding met broker, verlaat programma
    print("probleem verbinden broker")
    wifi.close()
    sys.exit()
#json.dumps zorgt ervoor dat dict een json string wordt
payload = json.dumps({"espname":ESP_NAME,"mac":MAC}).encode()
print(payload)
for i in range(3000):
    mqtt.publish("data/cvo/mac",payload)#data/cvo/mac is de topic
    time.sleep(2)
wifi.close()


    
    
    
    