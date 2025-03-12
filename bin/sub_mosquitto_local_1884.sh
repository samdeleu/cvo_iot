#!/usr/bin/env bash

MQTT_HOST="192.168.0.192"
MQTT_PORT=1884
MQTT_USER="samsam"
MQTT_PW="H3tCv0.be"
TOPIC_HOMEASSISTANT="homeassistant/#"
TOPIC_HOME="home/#"

echo "Listening on ${MQTT_HOST}:${MQTT_PORT} topic: ${TOPIC}"
mosquitto_sub \
  --host ${MQTT_HOST} --port ${MQTT_PORT} \
  --username ${MQTT_USER} --pw ${MQTT_PW} \
  --id "sam-hp" \
  --topic "${TOPIC_HOMEASSISTANT}" \
  --topic "${TOPIC_HOME}" \
  --pretty
echo "STOPPED listening on ${MQTT_HOST}:${MQTT_PORT} topic: ${TOPIC}"
