#!/usr/bin/python3
#FirstTesting.py

import bluetooth
from bluetooth.ble import DiscoveryService

print("Scan Blue Tooth")

nearby_devices = bluetooth.discover_devices()

print("found %d devices" % len(nearby_devices))

for bdaddr in nearby_devices:
    print(bluetooth.lookup_name( bdaddr ))

print("Scan BLE")

service = DiscoveryService("hci0")
devices = service.discover(2)

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))

# RFCOMM Server
print("Server")

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_sock.bind(("",port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

data = client_sock.recv(1024)
print ("received [%s]" % data)

client_sock.close()
server_sock.close()