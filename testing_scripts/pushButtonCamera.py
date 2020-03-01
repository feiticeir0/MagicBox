import picamera
from time import sleep
from RPi import GPIO

takeButton = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(takeButton, GPIO.IN, GPIO.PUD_UP)

camera = picamera.PiCamera()
camera.resolution = (1920,1080)
camera.start_preview()
GPIO.wait_for_edge(takeButton,GPIO.FALLING)
camera.capture('pushTesting.jpg')
camera.stop_preview()
