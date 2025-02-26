#!/usr/bin/env bash

MQTT_HOST="192.168.0.192"
MQTT_PORT=1884
MQTT_USER="samsam"
MQTT_PW="H3tCv0.be"
TOPIC="#"

echo "Listening on ${MQTT_HOST}:${MQTT_PORT} topic: ${TOPIC}"
mosquitto_sub \
  --host ${MQTT_HOST} --port ${MQTT_PORT} \
  -u ${MQTT_USER} -P ${MQTT_PW} \
  --topic ${TOPIC} \
  --pretty
echo "STOPPED listening on ${MQTT_HOST}:${MQTT_PORT} topic: ${TOPIC}"
