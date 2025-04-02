import sys
import random #om een willekeurig getal te genereren. Om dit te sturen
import ssl #Secure Socket Layer. Voor encrypteren van data ....
import time

from machine import Pin
from umqtt.robust import MQTTClient #module voor MQTT

from lib import simpleWifi_v2


MQTT_SERVER = "192.168.0.192"
MQTT_PORT = 1884
# MQTT_SERVER = "cb1801cd6d3b48339e06180cc5a759ff.s1.eu.hivemq.cloud"
# MQTT_PORT = 8883
MQTT_USER = "samsam"
MQTT_PW = "H3tCv0.be"

STATE_TOPIC = "home/lab/led1"
COMMAND_TOPIC = "home/lab/led1/set"
AVAILABILITY_TOPIC = "home/lab/led1/available"

led_board=Pin(2,Pin.OUT)
led_rood = Pin(14, Pin.OUT)
led_groen = Pin(13, Pin.OUT)

MQTT = None


def ha_cmd(topic, msg):
    topic = topic.decode()
    msg = msg.decode()
    led_board.value(1)
    print(f"Receiving on {topic}: {msg}")

    if "led1/set" in topic:
        if msg == "on":
            print("Received led1/set")
            led_rood.value(1)
        else:
            print("Received other then led1/set")
            led_rood.value(0)

    MQTT.publish(STATE_TOPIC, str(led_rood.value()).encode())
    led_board.value(0)


def mqtt_connect():
    #laat veiligheid over aan de server = Broker in de cloud
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_NONE
    mqttcl = MQTTClient(
            client_id="sam_esp_1".encode(),
            server=MQTT_SERVER.encode(),
            port=MQTT_PORT,  # 0 wijst naar de standaard poort, dat is 8883
            user=MQTT_USER.encode(),
            password=MQTT_PW.encode(),
            keepalive=7200, #connectie wordt 7200 seconden opengehouden
            ssl=None,
    )
    mqttcl.connect()
    return mqttcl

wifi = simpleWifi_v2.Wifi()

wifi.open()
if wifi.get_status() > 0:
    print("progr connected")
    print(wifi.get_IPdata())
else:
    print("progr not connected")
    sys.exit()
    
for i in range(5): #5x proberen connecteren met broker
    try:
        MQTT = mqtt_connect()
        break #als het lukt wordt de lus verlaten
    except Exception as Err:
        print("mqtt connection failed",Err)
        time.sleep(2)
if MQTT == None:#geen mqtt connectie, dus verlaat programma
    print("No mqtt connection possible")
    sys.exit()

# Instellen van callback functie om HomeAssistant
MQTT.set_callback(ha_cmd)
MQTT.subscribe(COMMAND_TOPIC)

# Geef een seintje als je klaar bent
for i in range(5):
    led_board.value(1)
    led_groen.value(1)
    led_rood.value(1)
    time.sleep(0.5)

    led_groen.value(0)
    led_rood.value(0)
    led_board.value(0)
    time.sleep(0.5)
    
while True:
    print(f"send: online on {AVAILABILITY_TOPIC}")
    MQTT.publish(AVAILABILITY_TOPIC,"online".encode())
    print(f" ... done: waiting on next message")
    MQTT.wait_msg()

