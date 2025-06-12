import network
import espnow
import time

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.WLAN.IF_STA)  # Or network.WLAN.IF_AP
sta.active(True)
sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b'\x08\xD1\xF9\x3A\xD7\x5C'   # MAC address of peer's wifi interface
broadcast = b'\xff\xff\xff\xff\xff\xff'   # MAC address of peer's wifi interface
e.add_peer(broadcast)      # Must add_peer() before send()
e.add_peer(peer)      # Must add_peer() before send()

e.send(peer, "Starting...")
for i in range(100):
    print("...")
    e.send(broadcast, str(i)*20, True)
    time.sleep(0.5)
e.send(peer, b'end')