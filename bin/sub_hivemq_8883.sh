#!/usr/bin/env bash

MQTT_HOST="cb1801cd6d3b48339e06180cc5a759ff.s1.eu.hivemq.cloud"
MQTT_PORT=8883
MQTT_USER="samsam"
MQTT_PW="H3tCv0.be"
TOPIC="samsam/#"

echo "Listening on ${MQTT_HOST}:${MQTT_PORT} topic: ${TOPIC}"
mosquitto_sub  \
    --host ${MQTT_HOST} --port ${MQTT_PORT} \
    -u ${MQTT_USER} -P ${MQTT_PW} \
    --topic ${TOPIC}
echo "STOPPED listening on ${MQTT_HOST}:${MQTT_PORT} topic: ${TOPIC}"
