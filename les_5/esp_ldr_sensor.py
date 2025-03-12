import sys
import time
import json

from machine import Pin, ADC, SoftI2C, I2C
from lib.ssd1306 import SSD1306_I2C
from lib import simpleWifi_v2
from lib.connectMQTT import mqtt_connect_mosquitto_local

print("### ESP32 with LDR Sensor in HomeAssistant ###")
i2c_face = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled = SSD1306_I2C(width=128, height=64, i2c=i2c_face, addr=0x3C)

oled.fill(1)
oled.show()
time.sleep(1)
oled.fill(0)
oled.show()

mqtt = None
DEV_NAME = "esp_ldr_sensor_sam"
SENSOR_ID = "19640927"

# Definitie van de sensor
ldr = ADC(Pin(36))
ldr.atten(ADC.ATTN_11DB)
def display_status(oled_device, status_msg):
    print(status_msg)
    oled_device.fill_rect(0, 54, 127, 63, 0)
    oled_device.text(status_msg, 0, 55, 1)
    oled_device.hline(0, 54, 127, 1)
    oled_device.show()
    
    
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
    display_status(oled, "Pub")
    client.publish(
        discovery_topic.encode(),
        json.dumps(discovery_payload).encode(),
        retain=True)
    print("auto discovery message send to HomeAssistant")        
        
display_status(oled, "Wifi connect")
wifi = simpleWifi_v2.Wifi()

wifi.open()
if wifi.get_status() > 0:
    display_status(oled, "Wifi CONNECTED")
    print(wifi.get_IPdata())
else:
    display_status(oled, "Wifi FAIL bye")
    sys.exit()

display_status(oled, "MQTT connect")
mqtt = mqtt_connect_mosquitto_local()
if mqtt is None:
    display_status(oled, "MQTT FAIL bye")
    sys.exit()

display_status(oled, "OP READY")
publish_discovery(mqtt, DEV_NAME, SENSOR_ID)

while True:
    val = ldr.read()
    val_percent = 100 * (val/2**12)  # 2**12 = 4096
    payload = {
        "ldr0": round(val_percent, 2)
    }
    print(f"   __ waarde ldr0: {val_percent}")
    oled.text(f"{val_percent:}%", 0, 0, 1)
    oled.hline(0, 8, 127, 1)
    if val_percent < 20:
        oled.text(f"<20 -> ON", 0, 12, 1)
    elif val_percent > 50:
        oled.text(f">50 -> OFF", 0, 12, 1)
    oled.hline(0, 20, 127, 1)
    oled.show()
    mqtt.publish(
        f"home/{DEV_NAME}/state",
        json.dumps(payload).encode()
    )
    time.sleep(2)
    oled.fill(0)
    oled.show()