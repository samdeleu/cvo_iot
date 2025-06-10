from simpleWifi_v2 import Wifi
import socket
import sys
import time

wifi = Wifi()
wifi.open()
if wifi.get_status() < 0:
    print("probleem connectie wifi")
    sys.exit()
print("verbinding met wifi")

SERVER = "192.168.0.117" #ip-adres van PC waarop node-red draait
PORT = 7555

while True:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#maken van een tcp/ip socket
    s.connect((SERVER,PORT)) #verbinden met socket server (die zal draaien op node-red)
    data = "test filip"
    s.send(data.encode())#zenden van data als bytearray
    s.close()#sluiten van de socket
    time.sleep(0.5)
    