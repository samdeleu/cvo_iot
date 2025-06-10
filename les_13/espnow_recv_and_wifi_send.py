import json
import network
import espnow
import time
import uasyncio as asyncio
import ubinascii
from simpleWifi_v2 import Wifi
#of anders:
#import simpleWifi_v2
#wifi = simpleWifi_v2.Wifi()
import sys
import socket

wifi = Wifi()
wifi.open()
if wifi.get_status() < 0:
    print("probleem connectie wifi")
    sys.exit()
print("verbinding met wifi")
wifi.net.config(pm=0)

SERVER = "192.168.0.160" #ip-adres van PC waarop node-red draait
PORT = 7555
QUEUE = [] #lijst om boodschappen in te stoppen
#CNT = 0 #id count of id bij bericht
#times_to_send = 2#aantal maal dat dezelfde boodschap wordt gestuurd


addrs = None
with open("macs.json","r") as f:#laden json bestand
    addrs = json.load(f)

print("mac adressen:",addrs)

#maken van opzoektabel (dictionary) mac --> naam esp
macs = []
names = []
for a in addrs:
    macs.append(a["mac"])
    names.append(a["espname"])

mac2name = dict(zip(macs,names))
###################################################

#voordat we ESPNOW kunnen gebruiken, moeten we wifi module
#activeren
net = network.WLAN(network.WLAN.IF_STA)
net.active(True)#activatie netwerk module
net.disconnect()

#espnow object maken voor het ontvangen
espnet_recv = espnow.ESPNow()
espnet_recv.active(True)

#toevoegen van de mac adressen ontvangers aan het espnow object
#of toevoegen van clients of peers
#for a in addrs:
    #a is een dictionary {"espname":test,"mac":"AAAAAAAAA"}
    # om het mac adres te krijgen wordt dit a["mac"]
    #Om het mac adres door te geven aan het espnow object
    #moet de string omgezet worden in een bytearray
#    x = bytearray.fromhex(a["mac"])
#    print(x)
#    espnet_send.add_peer(x)

async def send_socket():#asynchrone functie om met wifi te zenden
    print("start van socket zender")
    global QUEUE,SERVER,PORT
    while True:
        if len(QUEUE) == 0: #niets in de queue, wacht 0,05 seconden
            await asyncio.sleep(0.05)
            continue #terug begin while lus
        print("--------queue in socket functie--------")
        print(QUEUE)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#maken van een tcp/ip socket
        s.connect((SERVER,PORT)) #verbinden met socket server (die zal draaien op node-red)
        data = QUEUE.pop(0) #1ste element uit de queue poppen
        s.send(data.encode())#zenden van data als bytearray
        s.close()#sluiten van de socket
        await asyncio.sleep(0.05) #taak laten wachten voor andere taak

async def recv():#nodig om ontvangen asynchroon te maken (voor ESPNOW)
    #luistert 50 ms, gaat ook 50 ms in wacht zodat andere taken de
    #kans krijgen om uitgevoerd te worden.
    host = None;msg = None
    host,msg = espnet_recv.recv(50) #ontvanger staat 50ms
    #te luisteren
    return host,msg

async def getmsg(tblmac2name):
    global QUEUE
    print("start ontvanger")
    while True:
        host,msg = await recv()#hier wordt async recv() opgeroepen
        print(host,":",msg)
        if msg is not None and host is not None:
            host = ubinascii.hexlify(host).decode()
            print("ontvangen boodschap:",msg.decode(),"van:",tblmac2name[host])
            QUEUE.append(tblmac2name[host]+":"+msg.decode())#boodschap + zender
            #in queue stoppen
            QUEUE = list(set(QUEUE))
            #met de functie set worden dubbels uit de lijst QUEUE verwijderd.
            #Terzelfde tijd wordt de QUEUE ook een set object.
            #de set wordt terug geconverteerd naar lijst door gebruik te maken van list
        await asyncio.sleep(0.5)

loop = asyncio.get_event_loop()#task manager opstarten
loop.create_task(send_socket())#taken toevoegen
loop.create_task(getmsg(mac2name))
loop.run_forever()#task manager loopt "eeuwig"
    
    
    
    
    
    
    
    

    