#!/usr/bin/python3

"""
This program is used as a listener for power button
that controls how the printer will shutdown.


Power ON
	1. Supply GPIO7 (RPI Pin26) with 3.3V
	2. Upon booting, GPIO14 (RPI Pin8) must have 3.3v

Power Off
	1. Supply GPIO7 (RPI Pin26) with 3.3V for 5secs

DO NOT EDIT OR MODIFY THIS FILE
G3D Software Development Team
"""

import RPi.GPIO as GPIO
import os
import time

HOLD_DELAY_SECS = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def shutoff(channel):
    now  = 0
    start = time.time()
	
    while now < HOLD_DELAY_SECS and GPIO.input(26):
	
        now = (time.time() - start)

        if now >= HOLD_DELAY_SECS and GPIO.input(26):
            
            print("Shutting down...")
            os.system("sudo poweroff")
            break
		
GPIO.add_event_detect(26, GPIO.RISING, callback = shutoff, bouncetime = 200)

while True:
    # Start a loop with delay and just 
    # listen to button events
    print("Listening for button press...")
    time.sleep(1)
