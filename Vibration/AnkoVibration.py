#!/usr/bin/python3
#AnkoVibrtion.py

# import mqtt client
from paho.mqtt import client as mqtt_client

import random
import json


import threading
import time

count = 0

broker = 'localhost'
port = 1883
topic = "status/fctrl/s01"
client_id = f'subscribe-{random.randint(0, 100)}'

renew = False

data = {
    "Version":2,
    "DataCount": 0,
    "RPM": 0,
    "X-OA":0.000,
    "X-Band1":0.000,
    "X-Band2":0.000,
    "X-Band3":0.000,
    "Y-OA":0.000,
    "Y-Band1":0.000,
    "Y-Band2":0.000,
    "Y-Band3":0.000,
    "Z-OA":0.000,
    "Z-Band1":0.000,
    "Z-Band2":0.000,
    "Z-Band3":0.000,
}

#mqtt connection
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

#mqtt subscribe
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global renew
        global data
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        document_string = msg.payload.decode()
        renew = True
        document = document_string.split('|')
        #print(document)
        if document[0] == 'V2':
            data['Version'] = 2
            data["DataCount"] = (int(document[1]) << 48) + (int(document[2]) << 32) + (int(document[3]) << 16) + (int(document[4]))
            data['RPM'] = int(document[10])
            data['X-OA'] = float((int(document[11]) << 16) + (int(document[12]))) * 0.001
            data['Y-OA'] = float((int(document[13]) << 16) + (int(document[14]))) * 0.001
            data['Z-OA'] = float((int(document[15]) << 16) + (int(document[16]))) * 0.001
            data['X-Band1'] = float((int(document[17]) << 16) + (int(document[18]))) * 0.001
            data['X-Band2'] = float((int(document[19]) << 16) + (int(document[20]))) * 0.001
            data['X-Band3'] = float((int(document[21]) << 16) + (int(document[22]))) * 0.001
            data['Y-Band1'] = float((int(document[25]) << 16) + (int(document[26]))) * 0.001
            data['Y-Band2'] = float((int(document[27]) << 16) + (int(document[28]))) * 0.001
            data['Y-Band3'] = float((int(document[29]) << 16) + (int(document[30]))) * 0.001
            data['Z-Band1'] = float((int(document[33]) << 16) + (int(document[34]))) * 0.001
            data['Z-Band2'] = float((int(document[35]) << 16) + (int(document[36]))) * 0.001
            data['Z-Band3'] = float((int(document[37]) << 16) + (int(document[38]))) * 0.001
        else:
            data['Version'] = 1


    client.subscribe(topic)
    client.on_message = on_message

def ShowMessage():
    print(f"Version: {data['Version']}")
    print(f"Data Count :{data['DataCount']}")
    print(f"RPM :{data['RPM']}")
    print(f"X-OA: {data['X-OA']}; X-Band1: {data['X-Band1']}; X-Band2: {data['X-Band2']}; X-Band3: {data['X-Band3']}")
    print(f"Y-OA: {data['Y-OA']}; Y-Band1: {data['Y-Band1']}; Y-Band2: {data['Y-Band2']}; Y-Band3: {data['Y-Band3']}")
    print(f"Z-OA: {data['Z-OA']}; Z-Band1: {data['Z-Band1']}; Z-Band2: {data['Z-Band2']}; Z-Band3: {data['Z-Band3']}")

def DoWork():
    global count
    global renew

    while True:
        if renew == True:
            print("\033c", end='')
            print(count)
            count = count + 1
            renew = False
            ShowMessage()


        time.sleep(1)

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':

    myThread = threading.Thread(target=DoWork)
    myThread.start()
    run()



