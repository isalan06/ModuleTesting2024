#!/usr/bin/python3
#MQTTClient2MongoDB.py

# import MongoClient
from pymongo import MongoClient

import random
import json

# import mqtt client
from paho.mqtt import client as mqtt_client


broker = '192.168.100.199'
port = 1883
topic = "status/test"
topic2 = "status/update"
topic3 = "status/download"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

# Creating a client
client = MongoClient("localhost", 27017)
 
# Creating a database name GFG
db = client["updatetesting"]
coil = db["status"]

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        document_string = msg.payload.decode()
        document = json.loads(document_string)
        coil.insert_one(document)



    client.subscribe(topic)
    client.subscribe(topic2)
    #client.subscribe(topic3)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()