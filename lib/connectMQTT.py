from umqtt.robust import MQTTClient #module voor MQTT
import ssl

MQTT_SERVER = "192.168.0.192"
MQTT_PORT = 1884

MQTT_SERVER_HIVE = "cb1801cd6d3b48339e06180cc5a759ff.s1.eu.hivemq.cloud"
MQTT_PORT_HIVE = 8883

MQTT_USER = "samsam"
MQTT_PW = "H3tCv0.be"


def mqtt_connect_hivemq_cloud():
    #laat veiligheid over aan de server = Broker in de cloud
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_NONE
    mqttcl = MQTTClient(
            client_id="sam_esp_1".encode(),
            server=MQTT_SERVER_HIVE.encode(),
            port=MQTT_PORT_HIVE,  # 0 wijst naar de standaard poort, dat is 8883
            user=MQTT_USER.encode(),
            password=MQTT_PW.encode(),
            keepalive=7200, #connectie wordt 7200 seconden opengehouden
            ssl=context,
    )
    mqttcl.connect()
    return mqttcl

def mqtt_connect_public_hivemq():
    #laat veiligheid over aan de server = Broker in de cloud
    mqttcl = MQTTClient(
            client_id="sam196409271".encode(),
            server="broker.hivemq.com")
    mqttcl.connect()
    return mqttcl

def mqtt_connect_mosquitto_local():
    #laat veiligheid over aan de server = Broker in de cloud
    print("Connecting to mosquitto local")
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_NONE
    mqttcl = MQTTClient(
            client_id="sam_esp_1".encode(),
            server=MQTT_SERVER.encode(),
            port=MQTT_PORT,  # 0 wijst naar de standaard poort, dat is 8883
            user=MQTT_USER.encode(),
            password=MQTT_PW.encode(),
            keepalive=7200, #connectie wordt 7200 seconden opengehouden
            ssl=None,
    )
    mqttcl.connect()
    return mqttcl
