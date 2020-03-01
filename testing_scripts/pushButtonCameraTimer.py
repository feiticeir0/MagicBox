import picamera
from time import sleep
from RPi import GPIO

takeButton = 17
led1 =  27
led2 = 22
led3 = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(takeButton, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(led3,GPIO.OUT)

def timer():
	GPIO.output(led1,True)
	sleep(1)
	GPIO.output(led2,True)
	sleep(1)
	GPIO.output(led3,True)
	sleep(1)

def offLeds():
	GPIO.output(led3,False)
	GPIO.output(led2,False)
	GPIO.output(led1,False)

camera = picamera.PiCamera()
camera.resolution = (1920,1080)
camera.start_preview()
GPIO.wait_for_edge(takeButton,GPIO.FALLING)
timer()
camera.capture('pushTesting.jpg')
camera.stop_preview()
offLeds()
GPIO.cleanup()

