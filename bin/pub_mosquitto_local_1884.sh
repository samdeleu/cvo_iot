#!/usr/bin/env bash

MQTT_HOST="192.168.0.192"
MQTT_PORT=1884
MQTT_USER="samsam"
MQTT_PW="H3tCv0.be"
TOPIC="home"

while true
do
  MSG="8883-$(date +'%F %_H:%M:%S')-AAA"
  echo "sending...${MSG}"
  mosquitto_pub  \
	--host ${MQTT_HOST} --port ${MQTT_PORT} \
	-u ${MQTT_USER} -P ${MQTT_PW} \
	--topic "${TOPIC}" \
	--message "${MSG}"
  sleep 5
done
