"""
TODO:
    - refactor the code to use less globals
    - standardize the setup of the different components similar to arduino setup()
"""
import sys
import time
import json

from machine import Pin, ADC, SoftI2C, I2C
from dht import DHT11
from lib.ssd1306 import SSD1306_I2C
from lib import simpleWifi_v2
from lib.connectMQTT import mqtt_connect_mosquitto_local

print("### LDR Sensor, DHT11 Sensor met automatisatie in HomeAssistant ###")

# Lokaal oled schermpje
i2c_face = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled = SSD1306_I2C(width=128, height=64, i2c=i2c_face, addr=0x3C)

oled.fill(1)
oled.show()
time.sleep(1)
oled.fill(0)
oled.show()

# mqtt client object
mqtt = None

# CONSTANTS
LDR_DEV_NAME = "sam_ldr"
LDR_SENSOR_ID = "19640927"
DHT11_DEV_NAME = "sam_dht11"
DHT11_SENSOR_ID = "19640927"

# Definitie van de LDR sensor
ldr = ADC(Pin(36))
ldr.atten(ADC.ATTN_11DB)

# Definitie van de DHT11 sensor
dht11 = DHT11(Pin(23))

def display_status(oled_device, status_msg):
    """ display een status message op de onderste lijn van de oled"""
    
    print(status_msg)
    oled_device.fill_rect(0, 54, 127, 63, 0)
    oled_device.text(status_msg, 0, 55, 1)
    oled_device.hline(0, 54, 127, 1)
    oled_device.show()
    
    
# Functie auto detectie van de sensor in HomeAssistant
def publish_discovery(client, dev_name, uid, tag_name, unit):
    """ Voor elke meetwaarde (tag) moet blijkbaar een aparte config message worden gestuurd.
        Deze is {dev_name}_{tag_name}
        Ik heb dit afgeleid uit het voorbeeld op https://www.home-assistant.io/integrations/mqtt/#discovery-examples-with-component-discovery
        (Configuration topic no1: homeassistant/sensor/sensorBedroomT/config)
        
        De [device][identifiers] en [device][name] zijn dezelfde voor de tags temperature en humidity 
    """
    discovery_topic = f"homeassistant/sensor/{dev_name}_{tag_name}/config"
    discovery_payload = {
        "name": f"{dev_name}_{tag_name}",
        "state_topic": f"home/{dev_name}/state",
        "unit_of_measurement": f"{unit}",
        "unique_id": f"{dev_name}_{uid}_{tag_name}",
        "value_template": "{{ "+ f"value_json.{tag_name}" + " }}",  #ldr0 is de key om de waarde van ldr te publiceren
        "device": {
            "identifiers": [dev_name],
            "name": dev_name,
            "model": "ESP32",
            "manufacturer": "SamSam"
        },
        "origin": {
            "name": "esp32_sam",
        },
    }
    print(f"Publishing discovery message on: {discovery_topic}")
    display_status(oled, "Pub")
    client.publish(
        discovery_topic.encode(),
        json.dumps(discovery_payload).encode(),
        retain=True)
    print("auto discovery message send to HomeAssistant")        

#---------------
def handle_ldr(dev_name, tag_name, unit):
    """ lees de waarde van de ldr en publiceer de data """
    val = ldr.read()
    val_percent = 100 * (val/2**12)  # 2**12 = 4096
    payload = {
        f"{tag_name}": round(val_percent, 2)
    }
    print(f"   __ waarde {tag_name}: {val_percent}")
    oled.text(f"{val_percent:}{unit}", 0, 0, 1)
    oled.hline(0, 8, 127, 1)
    if val_percent < 20:
        oled.text(f"<20 -> ON", 0, 12, 1)
    elif val_percent > 50:
        oled.text(f">50 -> OFF", 0, 12, 1)
    oled.hline(0, 20, 127, 1)
    oled.show()
    mqtt.publish(
        f"home/{dev_name}/state",
        json.dumps(payload).encode()
    )

def handle_dht11(dev_name):
    """ lees de temperature en humidity van de ldr en publiceer de data """
    dht11.measure()
    temp = dht11.temperature()
    hum = dht11.humidity()
    payload = {
        "temperature": temp,
        "humidity": hum,
    }
    print(f"   __ payload: {payload}")
    mqtt.publish(
        f"home/{dev_name}/state",
        json.dumps(payload).encode()
    )
    
#---------------
# Probeer met de Wifi te verbinden
display_status(oled, "Wifi connect")
wifi = simpleWifi_v2.Wifi()

wifi.open()
if wifi.get_status() > 0:
    display_status(oled, "Wifi CONNECTED")
    print(wifi.get_IPdata())
else:
    display_status(oled, "Wifi FAIL bye")
    sys.exit()

# Probeer met de mqtt broker te verbinden
display_status(oled, "MQTT connect")
mqtt = mqtt_connect_mosquitto_local()
if mqtt is None:
    display_status(oled, "MQTT FAIL bye")
    sys.exit()

# Stuur een discovery message voor elke tag_name
display_status(oled, "OP READY")
publish_discovery(mqtt, LDR_DEV_NAME, LDR_SENSOR_ID, "ldr", "%")
publish_discovery(mqtt, DHT11_DEV_NAME, DHT11_SENSOR_ID, "humidity", "%")
publish_discovery(mqtt, DHT11_DEV_NAME, DHT11_SENSOR_ID, "temperature", "C")

while True:
    handle_ldr(LDR_DEV_NAME, "ldr", "%")
    handle_dht11(DHT11_DEV_NAME)
    time.sleep(2)
    oled.fill(0)
    oled.show()
