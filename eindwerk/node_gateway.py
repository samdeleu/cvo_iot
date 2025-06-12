""" Network node """
import aioespnow  # ESPNow met async support
import asyncio    # python async
import binascii
# import espnow
import network    # standaard network library
import sys


class Node:
    BROADCAST_ADDRESS = b'\xff\xff\xff\xff\xff\xff'
    
    def __init__(self):
        # De WLAN interface moet actief zijn om te kunnen zenden/ontvangen (send/recv
        self.nic = network.WLAN(network.WLAN.IF_STA)
        self.nic.active(True)
        self.nic.disconnect()  # For ESP8266
        
        # bepaal mijn eigen mac_address
        self.my_mac_address = binascii.hexlify(self.nic.config("mac")).decode()
        print(type(self.my_mac_address), self.my_mac_address)

        # activeer het espnow netwerk
        self.esp_net = aioespnow.AIOESPNow()  # ESPNow met async support
        self.esp_net.active(True)

        # voeg het broadcast address toe
        self.esp_net.add_peer(Node.BROADCAST_ADDRESS)

        # placeholder voor het huidige gateway address
        self.gateway_address = None
        
        # Event om te coordineren of een gateway gevonden is
        self.announce_sent_event = asyncio.Event()
        self.announced_event = asyncio.Event()

        # timeouts
        self.announce_period = 10

    async def receive(self):
        """ Ontvangen van messages en omzetten naar een actie """
        async for mac_sender, msg in self.esp_net:
            print(f"++++got -{msg}-")
            if msg:             # msg == None if timeout in recv()
                print(f"REC: {host}, {msg}")
                # split the binnenkomende boodschap
                # Deze heeft de vorm
                # COMMAND:PARAMETER_1:PARAMETER_2:PARAMETER_3:...:PARAMETER_N
                message = msg.decode().split(":")
                command = message[0]
                print(f"--> {message}")
                print(f"--> {command}")

                # fast stop
                if message == "STOP":
                    print("Stop receiving")
                    break
                
                # Antwoord op een announce met mijn eigen mac address om aan te geven dat ik een gateway ben
                if command == "ANNOUNCE":
                    # Als parameter wordt het MAC address van de peer verwacht
                    # hier moet een boodschap naartoe gestuurd worden met het MAC address van de gateway
                    node_mac_address = binascii.unhexlify(message[1])
                    print("...ANNOUNCE")
                    print("node_mac_address", node_mac_address)

                    esp.add_peer(node_mac_address)
                    esp.send(node_mac_address, f"GATEWAY:{self.my_mac_address}")
                
                # Een ping komt van een gateway die zoekt of ik nog aanwezig ben
                # Hierop moet met een PONG geantwoord worden
                if command == "PING":
                    # Als parameter wordt het MAC address van de peer verwacht
                    # hier moet een boodschap naartoe gestuurd worden met het MAC address van de gateway
                    node_mac_address = binascii.unhexlify(message[1])
                    print("...PING")
                    print("node_mac_address", node_mac_address)

                    try:
                        esp.send(node_mac_address, f"PONG:ALREADY PEERED")
                    except OSError as err:
                        if len(err.args) > 1 and err.args[1] == 'ESP_ERR_ESPNOW_NOT_FOUND':
                            esp.add_peer(node_mac_address)
                            esp.send(node_mac_address, f"PONG:IN CATCH")

        print("receive: before sleep")
        await asyncio.sleep(self.receive_delay)
        print("receive: after sleep")

    async def start(self, timeout=120):
        asyncio.create_task(self.receive())
        print("*******AA")
        await asyncio.sleep(timeout)
        print("*******ZZ")
        
if __name__ == "__main__":
    me = Node()
    asyncio.run(me.start())
