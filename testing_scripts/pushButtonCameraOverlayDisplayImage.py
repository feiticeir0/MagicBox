import picamera
from time import sleep
from RPi import GPIO
from PIL import Image

takeButton = 17
tweetButton = 23 
cancelButton = 24

led1 =  27
led2 = 22
led3 = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(takeButton, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(tweetButton, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(cancelButton, GPIO.IN, GPIO.PUD_UP)

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

camera = picamera.PiCamera()
camera.resolution = (1920,1080)
camera.framerate = 24
camera.start_preview()
GPIO.wait_for_edge(takeButton,GPIO.FALLING)
#timer()
overlayCounter()
camera.capture('pushTesting.jpg')
camera.stop_preview()

#display image
displayPreview('pushTesting.jpg')
# While not choosing an option
### Add a callback
####GPIO.add_event_detect(tweetButton,GPIO.FALLING,callback=tweetImage,bouncetime=300)
###while (True):
###	GPIO.wait_for_edge(cancelButton, GPIO.FALLING)
####	print ("cancelled Button")
##	break
GPIO.add_event_detect(tweetButton,GPIO.FALLING)
GPIO.add_event_detect(cancelButton,GPIO.FALLING)
while (True):
	if GPIO.event_detected(tweetButton):
		print "Tweet Button"
		break
	if GPIO.event_detected(cancelButton):
		print "Canceled"
		break


print ("Exited...")
#offLeds()
GPIO.cleanup()

