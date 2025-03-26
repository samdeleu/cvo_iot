from umqtt.robust import MQTTClient #module voor MQTT
import ssl #Secure Socket Layer. Voor encrypteren van data ....

def mqtt_connect_hivemq_cloud():
    #laat veiligheid over aan de server = Broker in de cloud
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_NONE
    mqttcl = MQTTClient(client_id="abc1234897".encode(),
                        server="cbe2a310c12b4b3590bbeed4579f37f8.s1.eu.hivemq.cloud".encode(),
                        port=0,#0 wijst naar de standaard poort, dat is 8883
                        user="cvo_filip_ds".encode(),
                        password="H3tCv0.be".encode(),
                        keepalive=7200, #connectie wordt 7200 seconden opengehouden
                        ssl=context
                        )
    mqttcl.connect()
    return mqttcl

def mqtt_connect_public_hivemq():
    mqttcl = MQTTClient("filiplkadeb9582396",
                        "broker.hivemq.com")
    mqttcl.connect()
    return mqttcl