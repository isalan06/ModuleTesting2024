#!/usr/bin/python3
#watermetertesting.py

import RPi.GPIO as GPIO
import time

wakeup_pin = 29

print("Initializing............")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(wakeup_pin, GPIO.OUT)

print("Trigger wake up HIGH.........")

GPIO.output(wakeup_pin, GPIO.HIGH)
time.sleep(0.005)

print("Trigger wake up LOW.........")

GPIO.output(wakeup_pin, GPIO.LOW)
time.sleep(0.001)

print("Send Message to")


GPIO.cleanup()

print("End of program!!!!")

