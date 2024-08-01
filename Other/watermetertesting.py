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

print("Initializing............")

GPIO.setmode(GPIO.BCM)
GPIO.setup(wakeup_pin, GPIO.OUT)

print("Trigger wake up HIGH.........")

GPIO.output(wakeup_pin, GPIO.HIGH)
time.sleep(0.005)

print("Trigger wake up LOW.........")

GPIO.output(wakeup_pin, GPIO.LOW)
time.sleep(0.001)

print("Send Message to")

GPIO.setup(RS485_EN,GPIO.OUT)
GPIO.output(RS485_EN,GPIO.HIGH)

t = serial.Serial("/dev/ttyS3",115200)    
print(t.portstr) 


GPIO.cleanup()

print("End of program!!!!")

