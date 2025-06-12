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
        print(f"...{type(self.my_mac_address)}, {self.my_mac_address}")

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
        self.receive_delay = 10
        self.data_period = 3
        
        # retries
        self.max_send_tries = 5

    #
    # De volgende handlers implementeren het communicatie-protocol tussen de verschillende nodes
    #
    def stop(self):
        print("Stopping all execution")
        sys.exit(0)

    async def handle_announce(self, peer_mac_address):
        # Als parameter wordt het MAC address van de peer verwacht
        # hier moet een boodschap naartoe gestuurd worden met het MAC address van de gateway
        print(f"handling ANNOUNCE for {peer_mac_address}: Do Nothing")
        await asyncio.sleep(0.1)
        
    async def handle_gateway(self, gateway_mac_address):
        # Als parameter wordt het MAC address van de peer verwacht
        # hier moet een boodschap naartoe gestuurd worden met het MAC address van de gateway
        print(f"handling GATEWAY for {gateway_mac_address}: Do Nothing")
        await asyncio.sleep(0.1)

    async def handle_data(self, data):
        # Als parameter wordt het MAC address van de peer verwacht
        # hier moet een boodschap naartoe gestuurd worden met het MAC address van de gateway
        print(f"handling DATA {data}: Do Nothing")
        await asyncio.sleep(0.1)

# Bij het opstarten wordt de node aangekondigd zodat eventuele gateways kunnen zien dat er een nieuwe
    # node is opgekomen.
    # Dit gebeurt door het uitsturen van een ANNOUNCE boodschap.
    async def announce(self):
        while True:
            self.announce_sent_event.clear()  # Blokkeer alle zenders totdat we we gateway hebben
            self.announced_event.clear()  # Blokkeer alle zenders totdat we we gateway hebben
            print("*Announcing myself")
            if not await self.esp_net.asend(Node.BROADCAST_ADDRESS, f"ANNOUNCE:{self.my_mac_address}"):
                print("Announce Broadcast: not responding:", Node.BROADCAST_ADDRESS)
            else:
                self.announce_sent_event.set()  # markeer dat we een announce hebben verzonden
                print(f"{self.announce_sent_event.is_set()=}")
            await asyncio.sleep(self.announce_period)

    async def receive(self):
        """ Ontvangen van messages en omzetten naar een actie """
        async for mac_sender, msg in self.esp_net:
            print(f"++++got -{msg}-")
            if msg:             # msg == None if timeout in recv()
                sender = binascii.hexlify(mac_sender).decode()
                # split the binnenkomende boodschap
                # Deze heeft de vorm
                # COMMAND:PARAMETER_1:PARAMETER_2:PARAMETER_3:...:PARAMETER_N
                message = msg.decode().split(":")
                command = message[0]
                print(f"  --> MESSAGE: {message}")
                print(f"  --> COMMAND: {command}")
                print(f"  --> MAC_SENDER:  {mac_sender}")
                print(f"  --> SENDER:  {sender}")

                # fast stop
                if message == "STOP":
                    self.stop()
                
                # Antwoord op een announce met mijn eigen mac address om aan te geven dat ik een gateway ben
                if command == "ANNOUNCE":
                    # Als parameter wordt het MAC address van de peer verwacht
                    # hier moet een boodschap naartoe gestuurd worden met het MAC address van de gateway
                    node_mac_address = binascii.unhexlify(message[1])
                    await self.handle_announce(node_mac_address)
                
                if command == "GATEWAY":
                    # Als parameter wordt het MAC address van de peer verwacht
                    # hier moet een boodschap naartoe gestuurd worden met het MAC address van de gateway
                    gateway_mac_address = binascii.unhexlify(message[1])
                    await self.handle_gateway(gateway_mac_address)

                if command == "DATA":
                    # Als parameter wordt het MAC address van de peer verwacht
                    # hier moet een boodschap naartoe gestuurd worden met het MAC address van de gateway
                    data = binascii.unhexlify(message[1])
                    await self.handle_data(data)

                # Een ping komt van een gateway die zoekt of ik nog aanwezig ben
                # Hierop moet met een PONG geantwoord worden
                if command == "PING":
                    # Als parameter wordt het MAC address van de peer verwacht
                    # hier moet een boodschap naartoe gestuurd worden met het MAC address van de gateway
                    node_mac_address = binascii.unhexlify(message[1])
                    await self.handle_ping
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

    async def collect_data(self):
        while True:
            print("*Sending data...")
            await self.announced_event.wait()  # Blokkeer alle zenders totdat we we gateway hebben
            print("*XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            data = "XXXX"
            
            if await self.esp_net.asend(self.gateway_address, f"DATA:{self.my_mac_address}:{data}"):
                print(f"DATA from {self.my_mac_address} send to gateway: {self.gateway_address}")
            else:
                print(f"Failed sending DATA from {self.my_mac_address} to gateway: {self.gateway_address}")
                
            await asyncio.sleep(self.data_period)

    async def send(self, mac, command, message):
        """ Functie om data proberen te zenden naar een mac address """
        trying_to_send = 0
        success = False
        while trying_to_send < self.max_send_tries:
            try:
                await self.esp_net.asend(mac, f"{command}:{message}")
                print(f"JUST have send: {command}:{message} to {mac}")
                trying_to_send = self.max_send_tries
                success = True
            except ValueError as v_err:
                print(f"Cannot handle {mac}: {v_err}")
                trying_to_send = self.max_send_tries
            except OSError as err:
                if len(err.args) > 1 and err.args[1] == 'ESP_ERR_ESPNOW_NOT_INIT':
                    # Niet geinitialiseerd
                    self.esp_net.active(True)
                if len(err.args) > 1 and err.args[1] == 'ESP_ERR_ESPNOW_IF':
                    # Peer is nog niet active()
                    self.esp_net.active(True)
                if len(err.args) > 1 and err.args[1] == 'ESP_ERR_ESPNOW_NO_MEM':
                    # Interne buffers zijn vol
                    Print("ERROR: interne buffer overflow, wat nu gedaan?")
                trying_to_send = trying_to_send + 1

        return success
    
    async def start(self, timeout=120):
        asyncio.create_task(self.announce())
        asyncio.create_task(self.receive())
        await asyncio.sleep(timeout)

# ------------------------------------------------------------------------------
class SensorNode(Node):
    """ Een node die via espnow is verbonden met een gateway om data door te sturen. """
    def __init__(self):
        print("Starting a SENSOR NODE")
        super().__init__()

    async def handle_gateway(self, gateway_mac_address):
        print(f"handling GATEWAY for {gateway_mac_address}")
        if self.announce_sent_event.is_set():
            # We hebben een announce uitgestuurd, dit is het antwoord (waarschijnlijk)
            print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
                        # Kijk of de peer al gekend is
            try:
                mac, lmk, channel, ifidx, encrypt = self.esp_net.get_peer(gateway_mac_address)
                print(f"Already have {mac} on channel -{channel}-")
            except ValueError as v_err:
                print(f"Cannot handle {gateway_mac_address}: {v_err}")
                can_send = False
            except OSError as os_err:
                if len(os_err.args) > 1 and os_err.args[1] == 'ESP_ERR_ESPNOW_NOT_FOUND':
                    self.esp_net.add_peer(gateway_mac_address)
            self.gateway_address = gateway_mac_address
            self.announced_event.set()  # Geef aan dat we een gateway hebben en data kunnen beginnen sturen
        await asyncio.sleep(0.1)

    async def start(self, timeout=120):
        asyncio.create_task(self.announce())
        asyncio.create_task(self.receive())
        asyncio.create_task(self.collect_data())
        await asyncio.sleep(timeout)

# ------------------------------------------------------------------------------
class GateWayNode(Node):
    """ Een node die zowel via espnow als via wifi verbonden is.
        Deze node moet alle ontvangen data naar de mqtt serever sturen """
    def __init__(self):
        print("Starting a GATEWAY NODE")
        super().__init__()

    async def handle_announce(self, peer_mac_address):
        # Als parameter wordt het MAC address van de peer verwacht
        # hier moet een boodschap naartoe gestuurd worden met het MAC address van de gateway
        print(f"handling ANNOUNCE for {peer_mac_address}")
        can_send = True
        
        # Kijk of de peer al gekend is
        try:
            mac, lmk, channel, ifidx, encrypt = self.esp_net.get_peer(peer_mac_address)
            print(f"Already have {mac} on channel -{channel}-")
        except ValueError as v_err:
            print(f"Cannot handle {peer_mac_address}: {v_err}")
            can_send = False
        except OSError as os_err:
            if len(os_err.args) > 1 and os_err.args[1] == 'ESP_ERR_ESPNOW_NOT_FOUND':
                self.esp_net.add_peer(peer_mac_address)
                
        # Zend eigen mac_address als gateway address
        if await self.send(peer_mac_address, "GATEWAY", self.my_mac_address):
            print("Success sending GATEWAY address")
        else:
            print("FAILED sending GATEWAY address")
            
            
        
if __name__ == "__main__":
    import config
    if config.ConfigData.node_type == "SensorNode":
        me = SensorNode()
    elif config.ConfigData.node_type == "GateWayNode":
        me = GateWayNode()

    asyncio.run(me.start())
