import picamera
import thread
import subprocess as sp

from time import sleep
from RPi import GPIO
from PIL import Image

# Button to take picture
takeButton = 17

# SocialNetwork Button
socialNetworkButton = 23 

# Cancel Picture
cancelButton = 24

# Take picture button LED
takePicButtonLed =  27
# Post to Social Network button LED
postSNLed = 22
# Cancel button LED
cancelButtonLed = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(takeButton, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(socialNetworkButton, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(cancelButton, GPIO.IN, GPIO.PUD_UP)

GPIO.setup(takePicButtonLed,GPIO.OUT)
GPIO.setup(postSNLed,GPIO.OUT)
GPIO.setup(cancelButtonLed,GPIO.OUT)

# Light only TakePicButtonLed
def onlyTakePicLed():
	GPIO.output(takePicButtonLed,True)
	GPIO.output(postSNLed,False)
	GPIO.output(cancelButtonLed,False)

# Light only Cancel and SocialNetwork button
def cancelPostLEDS():
	GPIO.output(takePicButtonLed,False)
	GPIO.output(postSNLed,True)
	GPIO.output(cancelButtonLed,True)


def countingTimerPicture():
	GPIO.output(takePicButtonLed,True)
	sleep(0.5)
	GPIO.output(takePicButtonLed,False)
	sleep(0.5)
	GPIO.output(takePicButtonLed,True)
	sleep(0.5)
	GPIO.output(takePicButtonLed,False)
	sleep(0.5)
	GPIO.output(takePicButtonLed,True)
	sleep(0.5)
	GPIO.output(takePicButtonLed,False)

def timer():
	GPIO.output(takePicButtonLed,True)
	sleep(1)
	GPIO.output(postSNLed,True)
	sleep(1)
	GPIO.output(cancelButtonLed,True)
	sleep(1)

def showAllLeds():
	GPIO.output(takePicButtonLed,True)
	GPIO.output(postSNLed,True)
	GPIO.output(cancelButtonLed,True)


def displayPreview(imgName):
	# Since the PIL image show is a crapp
	# we use the overlay from the camera to display
	# the preview

	img = Image.open(imgName)
	padding = Image.new('RGB', (
		((img.size[0] + 31) // 32) * 32,
		((img.size[0] + 15) // 16) * 16,
	))
	padding.paste(img, (0,0))
	ov = camera.add_overlay(padding.tostring(), size=img.size)
	ov.layer = 1

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

def tweetImage(channel):
	# Tweet the image
	print "Tweeting",imgName


# Main function
# Clear screen
tmp = sp.call('clear',shell=True)
camera = picamera.PiCamera()
camera.resolution = (1920,1080)
camera.framerate = 24
camera.start_preview()
#Show LED Only for Take Picture
onlyTakePicLed()
# Wait for button to take Picture
GPIO.wait_for_edge(takeButton,GPIO.FALLING)
#timer()
# Start a thread to count with the LEDs while the images are shown
# Probably could be used in the overlayCounter function,
# because it also as timers to show the pictures, but the led effects would not
# be the same
thread.start_new_thread ( countingTimerPicture,() )

# Show the pictures overlay in the camera picture
overlayCounter()
# Show all LEDS while taking the picture
showAllLeds()
camera.capture('pushTesting.jpg')
camera.stop_preview()

#display image
displayPreview('pushTesting.jpg')
# While not choosing an option
### Add a callback
####GPIO.add_event_detect(socialNetworkButton,GPIO.FALLING,callback=tweetImage,bouncetime=300)
###while (True):
###	GPIO.wait_for_edge(cancelButton, GPIO.FALLING)
####	print ("cancelled Button")
##	break
# Show LEDs to Cancel or Post to Social Networks
cancelPostLEDS()
GPIO.add_event_detect(socialNetworkButton,GPIO.FALLING)
GPIO.add_event_detect(cancelButton,GPIO.FALLING)
while (True):
	if GPIO.event_detected(socialNetworkButton):
		print "Tweet Button"
		break
	if GPIO.event_detected(cancelButton):
		print "Canceled"
		break


print ("Exited...")
#offLeds()
GPIO.cleanup()

