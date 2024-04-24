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
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        document_string = msg.payload.decode()

        if (msg.topic == topic) or (msg.topic == topic2):
            print('Record data to MongoDB')
            document = json.loads(document_string)
            coil.insert_one(document)
        else:
            print('Record data to MySQL')
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


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
    connect_db.close()