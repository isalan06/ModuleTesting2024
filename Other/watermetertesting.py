#!/usr/bin/python3
#watermetertesting.py

#sudo apt-get update
#sudo apt-get install python3-serial
#sudo apt-get install python3-can

import RPi.GPIO as GPIO
import time
import serial

RS485_EN =  4

wakeup_pin = 5

sp_baudrate = 9600

print("Initializing............")


GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(wakeup_pin, GPIO.OUT)

print("Trigger wake up HIGH.........")

GPIO.output(wakeup_pin, GPIO.HIGH)
time.sleep(0.005)

print("Trigger wake up LOW.........")

GPIO.output(wakeup_pin, GPIO.LOW)
time.sleep(0.001)

print("Initializing Serial...............")

GPIO.setup(RS485_EN,GPIO.OUT)
GPIO.output(RS485_EN,GPIO.HIGH)

t = serial.Serial("/dev/ttyS0",sp_baudrate)    
print(t.portstr + ";" + str(t.baudrate) + ";" + str(t.bytesize) + ";" + str(t.parity) + ";" + str(t.stopbits) + ";") 
t.reset_input_buffer()
t.reset_output_buffer()

senddata = [0x1, 0x3, 0x62, 0xD, 0x0, 0x0, 0x0, 0x0, 0x97, 0x44]

print("Send message: " + str(senddata))
t.write(senddata)

GPIO.output(RS485_EN,GPIO.LOW)

print("Start to read from serial port........")
try:
    while 1:
        dataarray = t.read()
        print (dataarray)

        time.sleep(0.01)
        #res = ''.join(format(x, '02x') for x in dataarray)
 
        # printing result
        #print("The string after conversion : " + str(res))
except KeyboardInterrupt:
    pass

GPIO.cleanup()

print("End of program!!!!")

