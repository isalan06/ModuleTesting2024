#!/usr/bin/python3
#MQTTClient2MongoDB.py

# import MongoClient
from pymongo import MongoClient

import random
import json

# import mqtt client
from paho.mqtt import client as mqtt_client

# import mysql
import pymysql

from MQTTClientAnalysis import MyData
from MQTTClientAnalysis import data_assembly

import threading
import time

myData = MyData()
count = 0

broker = 'localhost'
port = 1883
topic = "status/test"
topic2 = "status/update"
topic3 = "status/download"
topic4 = [("status/fctrl/y01",1),("status/fctrl/y02",1),("status/fctrl/y03",1),("status/fctrl/y04",1),("status/fctrl/y05",1)]
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

# Creating a client
client = MongoClient("localhost", 27017)
 
# Creating a database name GFG
db = client["updatetesting"]
coil = db["status"]

# Create a MySQL connection
connect_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='12345678', charset='utf8', db='anko_iot')

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
        global data_assembly
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        document_string = msg.payload.decode()

        if (msg.topic == topic) or (msg.topic == topic2):
            #print('Record data to MongoDB')
            document = json.loads(document_string)
            coil.insert_one(document)
        else:
            #print('Record data to MySQL')
            SetMessage(msg.topic, document_string)
            with connect_db.cursor() as cursor:
                sql = """
                INSERT INTO table_dio_record (record_time, topic, value) VALUES 
                (NOW(), '
                """
                sql += msg.topic
                sql +=  """
                        ','
                        """
                sql += document_string
                sql +=  """
                        ')
                        """
    
                # 執行 SQL 指令
                cursor.execute(sql)
    
                # 提交至 SQL
                connect_db.commit()

    client.subscribe(topic)
    client.subscribe(topic2)
    client.subscribe(topic4)
    client.on_message = on_message

def SetMessage(title, message):
    global data_assembly
    title_String = title.split('/')[2]
    for i in range(5):
        if data_assembly[i]['topic'] == title_String:
            data_array = message.replace(' ', '').replace('\n', '').split('|')
            data_assembly["hz_in"] = int(data_array[0])
            data_assembly["hz_out"] = int(data_array[1])
            data_assembly["a_out"] = int(data_array[2])
            data_assembly["rpm_out"] = int(data_array[3])
            data_assembly["temp"] = int(data_array[4])
            data_assembly["error"] = int(data_array[5])
            data_assembly["day"] = int(data_array[6])
            data_assembly["hour"] = int(data_array[7])
            break


def DoWork():
    global count

    while True:
        print("\033c", end='')
        print(count)
        myData.ShowMessage()
        count = count + 1

        """
        for i in range(10):

            message = '\rcount: ' + str(count)

            print(message, end="")
            count = count + 1

            time.sleep(1)
        """

        time.sleep(1)

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    myData.CreateData()
    myThread = threading.Thread(target=DoWork)
    myThread.start()
    #myRun = threading.Thread(target=run)
    run()
    connect_db.close()