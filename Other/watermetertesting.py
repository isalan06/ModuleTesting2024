#!/usr/bin/python3
#watermetertesting.py

import RPi.GPIO as GPIO
import time

wakeup_pin = 29

print("Initializing............")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(wakeup_pin, GPIO.OUT)

