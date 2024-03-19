#!/usr/bin/python3
#FirstTesting.py

import bluetooth
from bluetooth.ble import DiscoveryService
'''
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

'''
    

# RFCOMM Server
print("Server")

bluetooth.enable()

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

server_sock.bind(("",bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

print("Waiting for connection on RFCOMM channel", port)

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )



client_sock,address = server_sock.accept()
print("Accepted connection from ",address)

data = client_sock.recv(1024)
print ("received [%s]" % data)

client_sock.close()
server_sock.close()

