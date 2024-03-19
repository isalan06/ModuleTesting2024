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

service = DiscoveryService()
devices = service.discover(0)

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))