import sys
import RPi.GPIO as GPIO
import time

# Usage: python3 buzz.py num_beeps interval_sec

num_beeps = int(sys.argv[1])
interval_sec = float(sys.argv[2])
buzz_bcm_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzz_bcm_pin, GPIO.OUT)

for i in range(num_beeps):
    GPIO.output(buzz_bcm_pin, GPIO.HIGH)
    time.sleep(interval_sec)
    GPIO.output(buzz_bcm_pin, GPIO.LOW)
    time.sleep(interval_sec)    

GPIO.cleanup()

