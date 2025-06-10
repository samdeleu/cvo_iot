import simpleWifi_v2
import sys
import time
from connectMQTT import mqtt_connect_hivemq_cloud, mqtt_connect_mosquitto_local
import json #json structuur wordt verwacht door HA
from machine import Pin,ADC

mqtt = None
DEV_NAME = "esp32_pot_sensor_sam"
SENSOR_ID = "080270"
#potentiometer objecten maken
P1 = ADC(Pin(34))
P1.atten(ADC.ATTN_11DB)

P2 = ADC(Pin(39))
P2.atten(ADC.ATTN_11DB)

#functie auto detectie van esp sensor in HA
def publish_discovery(client):
    global DEV_NAME,SENSOR_ID
    #f (format) zorgt ervoor dat alles als een string kan geschreven worden
    #de waarden van variabelen kunnen in deze string worden ingevoegd door
    #de variabelen tussen {} te plaatsen.
    #vroeger deden we dit als volgt:
    #"homeassistant/sensor/"+str(DEV_NAME)+"/config"
    discovery_topic = f"homeassistant/sensor/{DEV_NAME}_pot1/config"
    discovery_payload = {
        "name":"potentiometer 1",
        "state_topic":f"home/{DEV_NAME}/state",#state topic device idem voor elke entiteit
        "unit_of_measurement":"%",
        "unique_id":f"{DEV_NAME}_{SENSOR_ID}_001",#moet uniek zijn
        "value_template":"{{value_json.pot1}}",#temp is hier de key om waarde
        #temperatuur te publiceren
        "device":{
            "identifiers":[DEV_NAME],
            "name":DEV_NAME,
            "model":"ESP32",
            "manufacturer":"Custom"}
        }
    client.publish(discovery_topic.encode(),
                   json.dumps(discovery_payload).encode(),
                   retain=True) #retain = True, zorgt ervoor dat deze boodschap
    #wordt behouden op de broker
    print("auto discovery pot1 naar HA gestuurd")
    
    discovery_topic = f"homeassistant/sensor/{DEV_NAME}_pot2/config"
    discovery_payload = {
        "name":"potentiometer 2",
        "state_topic":f"home/{DEV_NAME}/state",#aan HA zeggen wat state topic is
        "unit_of_measurement":"%",
        "unique_id":f"{DEV_NAME}_{SENSOR_ID}_002",
        "value_template":"{{value_json.pot2}}",#hum is hier de key om waarde
        #vochtigheid te publiceren
        "device":{
            "identifiers":[DEV_NAME],
            "name":DEV_NAME,
            "model":"ESP32",
            "manufacturer":"Custom"}
        }
    client.publish(discovery_topic.encode(),
                   json.dumps(discovery_payload).encode(),
                   retain=True) #retain = True, zorgt ervoor dat deze boodschap
    #wordt behouden op de broker
    print("auto discovery pot2 naar HA gestuurd")

wifi = simpleWifi_v2.Wifi()
wifi.open()
if wifi.get_status() < 0:#geen verbinding, verlaten prog
    print("geen connectie met het netwerk, bye ...")
    sys.exit()

print(wifi.get_IPdata())

#als je import doet van connectMQTT
#dus import connectMQTT
#dan moet de functie: mqtt_connect_hivemq_cloud() oproepen
#als volgt:
#connectMQTT.mqtt_connect_hivemq_cloud()
mqtt_hive = mqtt_connect_hivemq_cloud()
if mqtt_hive is None:#geen verbinding broker, verlaat prog
    print("geen connectie met de HIVEMQ broker, bye ...")
    sys.exit()

mqtt_local = mqtt_connect_mosquitto_local()
if mqtt_local is None:#geen verbinding broker, verlaat prog
    print("geen connectie met de lokale mosquito broker, bye ...")
    sys.exit()

publish_discovery(mqtt_hive)
publish_discovery(mqtt_local)

while True:
    value1 = P1.read()
    value1 = 100*value1//4096
    value2 = P2.read()
    value2 = 100*value2//4096
    payload = {"pot1":value1,"pot2":value2}
    mqtt_hive.publish(f"home/{DEV_NAME}/state",json.dumps(payload).encode())
    mqtt_local.publish(f"home/{DEV_NAME}/state",json.dumps(payload).encode())
    print("waarden potentiometers ","pot1:",payload["pot1"],"pot2:",payload["pot2"])
    time.sleep(2)

