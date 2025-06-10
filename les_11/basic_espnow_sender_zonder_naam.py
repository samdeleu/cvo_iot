import json
import network
import espnow
import time

esp_name = "esp_filiplk"

addrs = None
with open("macs.json","r") as f:#laden json bestand
    addrs = json.load(f)

print("mac adressen:",addrs)

#voordat we ESPNOW kunnen gebruiken, moeten we wifi module
#activeren
net = network.WLAN(network.WLAN.IF_STA)
net.active(True)#activatie netwerk module
net.disconnect()

#espnow object maken
espnet = espnow.ESPNow()
espnet.active(True)

#toevoegen van de mac adressen ontvangers aan het espnow object
#of toevoegen van clients of peers
for a in addrs:
    #a is een dictionary {"espname":test,"mac":"AAAAAAAAA"}
    # om het mac adres te krijgen wordt dit a["mac"]
    #Om het mac adres door te geven aan het espnow object
    #moet de string omgezet worden in een bytearray
    x = bytearray.fromhex(a["mac"])
    print(x)
    espnet.add_peer(x)

cnt_on = 1
cnt_off = 1
while True:
    try:
        res = espnet.send(f"cmd:LED=on,count on:{cnt_on}")
        print("verzonden?",res)
        cnt_on = cnt_on + 1 #of cnt_on+=1
    except:
        continue
    time.sleep(1)
    try:
        res = espnet.send(f"cmd:LED=off,count off:{cnt_off}")
        print("verzonden?",res)
        cnt_off = cnt_off + 1
    except:
        continue
    time.sleep(1)
    
    