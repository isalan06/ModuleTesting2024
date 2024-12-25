#!/usr/bin/python3
#MQTTClient2MySQL.py

# import mqtt client
from paho.mqtt import client as mqtt_client

# import mysql
import pymysql

import random
import json

broker = 'localhost'#'192.168.1.60'
port = 1883
topic = "status/fctrl/#"
client_id = f'subscribe-{random.randint(0, 100)}'

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
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()