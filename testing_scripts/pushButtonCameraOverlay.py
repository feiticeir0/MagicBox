import picamera
from time import sleep
from RPi import GPIO
from PIL import Image

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

# Function to overlay image
def overlayCounter():
	#load images
	img1 = Image.open('3.png')
	img2 = Image.open('2.png')
	img3 = Image.open('1.png')
	# Create an overlay
	# Used with img1 because all are the same size
	pad = Image.new('RGB', (
		((img1.size[0] + 31) // 32) * 32,
		((img1.size[1] + 15) // 16) * 16,
	))
	
	# paste the overlay - 3
	pad.paste(img1, (0,0))
	ov = camera.add_overlay(pad.tostring(), size=img1.size)
	ov.alpha = 200
	# layer is 3 because camera preview is on layer 2
	ov.layer = 3
	sleep(1)

	camera.remove_overlay(ov) 

	# paste the overlay - 2
	pad.paste(img2, (0,0))
	ov = camera.add_overlay(pad.tostring(), size=img2.size)
	ov.alpha = 200
	# layer is 3 because camera preview is on layer 2
	ov.layer = 3
	sleep(1)

	camera.remove_overlay(ov)
	
	# paste the overlay - 1
	pad.paste(img3, (0,0))
	ov = camera.add_overlay(pad.tostring(), size=img3.size)
	ov.alpha = 200
	# layer is 3 because camera preview is on layer 2
	ov.layer = 3
	sleep(1)
	camera.remove_overlay(ov)


camera = picamera.PiCamera()
camera.resolution = (1920,1080)
camera.framerate = 24
camera.start_preview()
GPIO.wait_for_edge(takeButton,GPIO.FALLING)
#timer()
overlayCounter()
camera.capture('pushTesting.jpg')
camera.stop_preview()
#offLeds()
GPIO.cleanup()

