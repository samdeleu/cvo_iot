import aioespnow  # ESPNow met async support
import asyncio    # python async
import binascii   # omzetten van en naar bin/hex/ascii
import network    # standaard network library
import sys

# De WLAN interface moet actief zijn om te kunnen zenden/ontvangen (senf/recv
nic = network.WLAN(network.WLAN.IF_STA)
nic.active(True)
nic.disconnect()    # For ESP8266

# bepaal mijn eigen mac_address
my_mac_address = binascii.hexlify(nic.config("mac")).decode()
print(type(my_mac_address), my_mac_address)

# activeer het espnow netwerk
esp_net = aioespnow.AIOESPNow()  # ESPNow met async support
esp_net.active(True)

# voeg het broadcast address toe
BROADCAST_ADDRESS = b'\xff\xff\xff\xff\xff\xff'
esp_net.add_peer(BROADCAST_ADDRESS)

# placeholder voor het gateway address
peer = b'\x08\xD1\xF9\x3A\xD7\x5c'
gateway_address = None



# Bij het opstarten wordt de node aangekondigd zodat de gateway kan zien dat er een nieuwe node is
# Dit gebeurt door het uitsturen van een ANNOUNCE boodschap.
async def announce(esp, period=10):
    global gateway_address
    global peer
    
    while True:
        if gateway_address is None:
            print("Announcing myself")
            if not await esp.asend(BROADCAST_ADDRESS, f"ANNOUNCE:{my_mac_address}"):
                print("Broadcast: not responding:", BROADCAST_ADDRESS)
            else:
                gateway_address = peer
                esp_net.add_peer(gateway_address)
                print("Broadcast: ", BROADCAST_ADDRESS)
        else:
            print(f"Already announced to: {gateway_address}")
        await asyncio.sleep(period)

# Als er een verbinding is met de gateway wordt op geregelde tijdstippen een heartbeat uitgestuurd
# zodat de gateway weet dat de node nog steeds actief is.
async def heartbeat(esp, period=10):
    global gateway_address
    
    while True:
        if gateway_address is not None:
            if not await esp.asend(gateway_address, f"PING:{my_mac_address}"):
                print("Heartbeat: gateway not responding:", gateway_address)
            else:
                print("Heartbeat: ping", gateway_address)
        else:
            print("Lost gateway:", gateway_address)
        await asyncio.sleep(period)

# Het behandelen van een ontvangen message
async def handle_message(esp):
    async for mac, msg in esp:
        print("mac:", mac)
        print("Echo:", msg)
        try:
            await esp.asend(mac, msg)
        except OSError as err:
            if len(err.args) > 1 and err.args[1] == 'ESP_ERR_ESPNOW_NOT_FOUND':
                esp.add_peer(mac)
                await esp.asend(mac, msg)

# Echo any received messages back to the sender
async def echo_server(esp):
    print("...... async echo start")
    async for mac, msg in esp:
        print("mac:", mac)
        print("Echo:", msg)
        try:
            await esp.asend(mac, msg)
        except OSError as err:
            if len(err.args) > 1 and err.args[1] == 'ESP_ERR_ESPNOW_NOT_FOUND':
                esp.add_peer(mac)
                await esp.asend(mac, msg)
    print("...... async echo stop")


async def main(esp, peer, timeout, period):
    asyncio.create_task(announce(esp, period))
    asyncio.create_task(heartbeat(esp, period))
    asyncio.create_task(echo_server(esp))
    print("AA")
    await asyncio.sleep(timeout)
    print("ZZ")

asyncio.run(main(esp_net, peer, 10, 3))