import simpleWifi_v2
import sys
import random #om een willekeurig getal te genereren. Om dit te sturen
from umqtt.robust import MQTTClient #module voor MQTT
import ssl #Secure Socket Layer. Voor encrypteren van data ....
import time
from machine import Pin

led1 = Pin(23,Pin.OUT)
led2 = Pin(22,Pin.OUT)

state_topic = "home/lab/led1"#topic om toestand pin door te sturen aan HA
command_topic = "home/lab/led1/set"#topic met commando HA aan ESP32
availability_topic = "home/lab/led1/available"#topic dat ESP gebruikt om
#aan HA (HomeAssitant) te zeggen dat hij online is
state_topic2 = "home/lab/led2"#topic om toestand pin door te sturen aan HA
command_topic2 = "home/lab/led2/set"#topic met commando HA aan ESP32
availability_topic2 = "home/lab/led2/available"#topic dat ESP gebruikt om
#aan HA (HomeAssitant) te zeggen dat hij online is
mqtt = None

def HA_CMD(topic,msg):
    
    topic = topic.decode()
    if "led1/set" in topic:#indien status led1 moet wijzigen
        msg = msg.decode()
        print("msg led1:"+msg)
        if msg == "on":#boodschap: on, led1 aan
            led1.value(1)
        else:
            led1.value(0)
        #doorgeven van de status van led1
        print("toestand led1:",str(led1.value()))
        mqtt.publish(state_topic,str(led1.value()).encode())
    if "led2/set" in topic:#indien status led1 moet wijzigen
        msg = msg.decode()
        print("msg led2:"+msg)
        if msg == "on":#boodschap: on, led1 aan
            led2.value(1)
        else:
            led2.value(0)
        #doorgeven van de status van led1
        print("toestand led2:",str(led2.value()))
        mqtt.publish(state_topic,str(led2.value()).encode())

def mqtt_connect():
    #laat veiligheid over aan de server led1/set= Broker in de cloud
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_NONE
    mqttcl = MQTTClient(client_id="abc1234897".encode(),
                        server="cbe2a310c12b4b3590bbeed4579f37f8.s1.eu.hivemq.cloud".encode(),
                        port=0,#0 wijst naar de standaard poort, dat is 8883
                        user="cvo_filip_ds".encode(),
                        password="H3tCv0.be".encode(),
                        keepalive=7200, #connectie wordt 7200 seconden opengehouden
                        ssl=context
                        )
    mqttcl.connect()
    return mqttcl

wifi = simpleWifi_v2.Wifi()
wifi.open() #ESP krijgt IP-adres van DHCP server
#Hieronder: ESP van een statisch adres voorzien
#eerste param: vast ip-adres, 2de subnetmask,3de ip adres router,4de dns
#wifi.open_static("192.168.77.201","255.255.255.0","192.168.77.1","192.168.77.1")
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
#instellen van callback functie om boodschappen van HA te
#ontvangen (via de Broker)
mqtt.set_callback(HA_CMD)
#subscribe command topic
mqtt.subscribe(command_topic)
mqtt.subscribe(command_topic2)

while True:
    #ESP32 staat ter beschikking = is online
    mqtt.publish(availability_topic,"online".encode())
    mqtt.publish(availability_topic2,"online".encode())
    mqtt.check_msg() #checken op inkomende boodschap
    time.sleep(0.05)
