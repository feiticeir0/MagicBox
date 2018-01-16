# Testing the big push button

from time import sleep
from RPi import GPIO

takeButton = 17
ledButton = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(takeButton, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(ledButton, GPIO.OUT)

# Make button signal is on
GPIO.output(ledButton,True)
GPIO.wait_for_edge(takeButton,GPIO.FALLING)
GPIO.output(ledButton,False)
GPIO.cleanup()
