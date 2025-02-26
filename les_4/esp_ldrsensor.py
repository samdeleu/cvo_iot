import sys
import time
import json

from machine import Pin, ADC

from lib import simpleWifi_v2
from lib.connectMQTT import mqtt_connect_mosquitto_local

print("### ESP32 with LDR Sensor in HomeAssistant ###")
mqtt = None
DEV_NAME = "esp_ldr_sensor_sam"
SENSOR_ID = "19640927"

# Definitie van de sensor
ldr = ADC(Pin(36))
ldr.atten(ADC.ATTN_11DB)

# Functie auto detectieim van de sensor in HomeAssistant
def publish_discovery(client, dev_name, uid):
    discovery_topic = f"homeassistant/sensor/{dev_name}/config"
    discovery_payload = {
        "name": f"LDR 0",
        "state_topic": f"home/{dev_name}/state",
        "unit_of_measurement": "%",
        "unique_id": f"{dev_name}_{uid}",
        "value_template": "{{ value_json.ldr0 }}",  #ldr0 is de key om de waarde van ldr te publiceren
        "device": {
            "identifiers": [dev_name],
            "name": dev_name,
            "model": "ESP32",
            "manufacturer": "SamSam"
        }
    }
    print("Publishing discovery message")
    client.publish(
        discovery_topic.encode(),
        json.dumps(discovery_payload).encode(),
        retain=True)
    print("auto discovery message send to HomeAssistant")        
        
print("Opening wifi")
wifi = simpleWifi_v2.Wifi()

wifi.open()
if wifi.get_status() > 0:
    print("wifi connected")
    print(wifi.get_IPdata())
else:
    print("wifi not connected, bye...")
    sys.exit()

print("Connecting to MQTT Broker")
mqtt = mqtt_connect_mosquitto_local()
if mqtt is None:
    print("No connection to MQTT Broker, bye...")
    sys.exit()

print("Ready to communicate :)")
publish_discovery(mqtt, DEV_NAME, SENSOR_ID)

while True:
    val = ldr.read()
    val_percent = 100 * (val/2**12)  # 2**12 = 4096
    payload = {
        "ldr0": round(val_percent, 2)
    }
    print(f"   __ waarde ldr0: {val_percent}")
    mqtt.publish(
        f"home/{DEV_NAME}/state",
        json.dumps(payload).encode()
    )
    time.sleep(2)