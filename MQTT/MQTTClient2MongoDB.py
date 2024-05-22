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
import MQTTClientAnalysis

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
topic5 = "status/fctrl/s01"
topic6 = "iot/topic"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

# Creating a client
mcclient = MongoClient("localhost", 27017)
 
# Creating a database name GFG
db = mcclient["updatetesting"]
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
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        document_string = msg.payload.decode()

        if (msg.topic == topic) or (msg.topic == topic2):
            #print('Record data to MongoDB')
            document = json.loads(document_string)
            coil.insert_one(document)
        elif msg.topic == topic6:
            pass
            document = json.loads(document_string)
            machine_name = document['topic']
            naber = document['naber']
            machine_title = machine_name + '_' + naber
            flag_name = document['status']
            topic_name = 'sensor'
            if flag_name[0:3] == 'z05':
                topic_name = 'vibration'
            db2 = mcclient[machine_title]
            coil2 = db2[topic_name]
            coil2.insert_one(document)
        elif msg.topic == topic5:
            with connect_db.cursor() as cursor:
                sql = """
                INSERT INTO table_dio_record2 (record_time, topic, value) VALUES 
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
        else:
            #print('Record data to MySQL')
            if msg.topic != topic5:
                #print (msg.topic)
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
    client.subscribe(topic5)
    client.subscribe(topic6)
    client.on_message = on_message

def SetMessage(title, message):
    title_String = title.split('/')[2]
    #print(len(MQTTClientAnalysis.data_assembly))
    for i in range(5):
        if len(MQTTClientAnalysis.data_assembly) <= i:
            break
        #print(MQTTClientAnalysis.data_assembly[i]['topic'])
        #print(title_String)
        if MQTTClientAnalysis.data_assembly[i]['topic'] == title_String:
            data_array = message.replace(' ', '').replace('\n', '').split('|')
            MQTTClientAnalysis.data_assembly[i]["hz_in"] = int(data_array[0])
            MQTTClientAnalysis.data_assembly[i]["hz_out"] = int(data_array[1])
            MQTTClientAnalysis.data_assembly[i]["a_out"] = int(data_array[2])
            MQTTClientAnalysis.data_assembly[i]["rpm_out"] = int(data_array[3])
            MQTTClientAnalysis.data_assembly[i]["temp"] = int(data_array[4])
            MQTTClientAnalysis.data_assembly[i]["error"] = int(data_array[5])
            MQTTClientAnalysis.data_assembly[i]["day"] = int(data_array[6])
            MQTTClientAnalysis.data_assembly[i]["hour"] = int(data_array[7])
            break


def DoWork():
    global count

    while True:
        print("\033c", end='')
        print(count)
        #print(len(MQTTClientAnalysis.data_assembly))
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