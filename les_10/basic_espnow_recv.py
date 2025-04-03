import network
import espnow

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.WLAN.IF_STA)
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

espnet = espnow.ESPNow()
espnet.active(True)

while True:
    print("Start receiving...")
    host, msg = espnet.recv()
    if msg:             # msg == None if timeout in recv()
        print(host, msg)
        if msg == b'end':
            break