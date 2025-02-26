#!/usr/bin/env bash

MQTT_HOST="cb1801cd6d3b48339e06180cc5a759ff.s1.eu.hivemq.cloud"
MQTT_PORT=8883
MQTT_USER="samsam"
MQTT_PW="H3tCv0.be"
TOPIC="samsam"

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
