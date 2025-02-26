import sys
import random #om een willekeurig getal te genereren. Om dit te sturen
import ssl #Secure Socket Layer. Voor encrypteren van data ....
import time

from umqtt.robust import MQTTClient #module voor MQTT

from lib import simpleWifi_v2

def mqtt_connect():
    #laat veiligheid over aan de server = Broker in de cloud
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_NONE
    mqttcl = MQTTClient(
            client_id="sam_esp_1".encode(),
            server="cb1801cd6d3b48339e06180cc5a759ff.s1.eu.hivemq.cloud".encode(),
            port=8883,#0 wijst naar de standaard poort, dat is 8883
            user="samsam".encode(),
            password="H3tCv0.be".encode(),
            keepalive=7200, #connectie wordt 7200 seconden opengehouden
            ssl=context,
    )
    mqttcl.connect()
    return mqttcl

wifi = simpleWifi_v2.Wifi()

wifi.open()
if wifi.get_status() > 0:
    print("connected")
    print(wifi.get_IPdata())
else:
    print("not connected")
    sys.exit()
    
mqtt = None
    
for i in range(5): #5x proberen connecteren met broker
    try:
        mqtt = mqtt_connect()
        break #als het lukt wordt de lus verlaten
    except Exception as Err:
        print("mqtt connection failed",Err)
        time.sleep(2)
        
if mqtt == None:#geen mqtt connectie, dus verlaat programma
    print("No mqtt connection possible")
    sys.exit()

while True:
    num = random.randint(0,900)
    mqtt.publish("cvo/data",str(num).encode())
    print("send:",num)
    time.sleep(2)
