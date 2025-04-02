from simpleWifi_v2 import Wifi
import sys
import socket
from mylibs.servos import ESP32Servo
import time

PORT = 7888

servo = ESP32Servo(23,0.4,2.5)
servo.start()
time.sleep(0.05)


wifi = Wifi()
wifi.open()
if wifi.get_status() <= 0:
    print("probleem verbinden wifi")
    sys.exit()

print("IP gegevens:",wifi.get_IPdata())

s = socket.socket()#socket object
s.bind(("0.0.0.0",PORT))#een poort aan de server toekennen
#server draait op ESP (0.0.0.0 = verwijzen naar zichzelf)
s.listen()#Luister naar de poort
while True:
    client,addr = s.accept()#binnenkomen vraag connectie
    #client verwijzing naar connectie en addr: IP adres van
    #client
    data = client.recv(32)#data ontvangen, 32 = plaats gereserveerd
    #voor buffer
    data = data.decode()#van bytes naar string
    print("data:",data)
    servo.move_to(int(data))
    client.close()#verbinding verbreken
