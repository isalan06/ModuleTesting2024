#!/usr/bin/python3
#FirstTesting.py

import bluetooth


nearby_devices = bluetooth.discover_devices()

print("found %d devices" % len(nearby_devices))

for bdaddr in nearby_devices:
    print(bluetooth.lookup_name( bdaddr ))