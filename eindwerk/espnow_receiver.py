import network
import espnow
import binascii


# De WLAN interface moet actief zijn om te kunnen zenden/ontvangen (send/recv
nic = network.WLAN(network.WLAN.IF_STA)
nic.active(True)
nic.disconnect()    # For ESP8266

# bepaal mijn eigen mac_address
my_mac_address = binascii.hexlify(nic.config("mac")).decode()
print(type(my_mac_address), my_mac_address)

esp = espnow.ESPNow()
esp.active(True)

COMMAND_LENGTH = 5
print("Start Receiving")
while True:
    host, msg = esp.recv()
    if msg:             # msg == None if timeout in recv()
       print(f"REC: {host}, {msg}")
       if msg == b'end':
            break

    # split the binnenkomende boodschap
    # Deze heeft de vorm
    # COMMAND:PARAMETER_1:PARAMETER_2:PARAMETER_3:...:PARAMETER_N
    message = msg.decode().split(":")
    command = message[0]
    print(f"--> {message}")
    print(f"--> {command}")
    
    if command == "ANNOUNCE":
        # Als parameter wordt het MAC address van de peer verwacht
        # hier moet een boodschap naartoe gestuurd worden met het MAC address van de gateway
        node_mac_address = binascii.unhexlify(message[1])
        print("...ANNOUNCE")
        print("node_mac_address", node_mac_address)

        esp.add_peer(node_mac_address)
        esp.send(node_mac_address, f"GATEWAY:{my_mac_address}")
        
    if command == "PING":
        # Als parameter wordt het MAC address van de peer verwacht
        # hier moet een boodschap naartoe gestuurd worden met het MAC address van de gateway
        node_mac_address = binascii.unhexlify(message[1])
        print("...PING")
        print("node_mac_address", node_mac_address)

        # esp.add_peer(node_mac_address)
        esp.send(node_mac_address, f"PONG:{my_mac_address}")
        
        try:
            esp.send(node_mac_address, f"PONG:ALREADY PEERED")
        except OSError as err:
            if len(err.args) > 1 and err.args[1] == 'ESP_ERR_ESPNOW_NOT_FOUND':
                esp.add_peer(node_mac_address)
                esp.send(node_mac_address, f"PONG:IN CATCH")
                
