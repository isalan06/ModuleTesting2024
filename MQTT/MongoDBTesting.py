#!/usr/bin/python3
#MQTTClientTesting.py

# import MongoClient
from pymongo import MongoClient
 
 
# Creating a client
client = MongoClient("localhost", 27017)
 
# Creating a database name GFG
db = client["updatetesting"]
coil = db["testing"]
document = {"Type": "Test"}
coil.insert_one(document)
print("Database is created !!")

print(client.list_database_names())