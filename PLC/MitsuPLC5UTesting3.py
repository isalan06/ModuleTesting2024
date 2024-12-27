#!/usr/bin/python3
#MitsuPLC5UTesting3.py

# 请先安装 pymodbus 和 pyserial
# pip install pymodbus
# pip install pyserial

import serial
import logging

UNIT = 0x1
serial_device = '/dev/tty.usbserial-120'

# 配置日志记录
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

import time

def main():

    print(f"Connect to Modbus Device({serial_device})")
    SerialObj = serial.Serial(serial_device) # COMxx format on Windows

    SerialObj.baudrate = 19200 # set Baud rate to 9600
    SerialObj.bytesize = 8 # Number of data bits = 8
    SerialObj.parity ='O' # No parity
    SerialObj.stopbits = 1 # Number of Stop bits = 1

    time.sleep(1)  

    values = bytearray([1, 3, 3, 232, 0, 3, 133, 187])
    print(f"Write Data({values})")
    SerialObj.write(values)

    print("Waiting......")

    response = SerialObj.read(11)
    print(f"Read Data: {response}")

    SerialObj.close() # Close the port
    print("Disconnect from Modbus Device")

 
 
 
if __name__ == "__main__":
    main()


