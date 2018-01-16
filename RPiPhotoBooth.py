# coding=utf-8

import picamera
import thread
import subprocess as sp
import time
import PIL

from time import sleep
from RPi import GPIO
from PIL import Image

import threading

# Twitter
import tweepy

# Facebook
import facebook


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

# Twitter settings
def get_api(cfg):
	auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
	auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
	return tweepy.API(auth)

# Send to twitter
def sendToTwitter():
	cfg = {
		"consumer_key"		: "",
		"consumer_secret"	: "",
		"access_token"		: "",
		"access_token_secret"	: ""
	}

	api = get_api(cfg)
	# Status Message
	tweet = "Message to send to twitter"
	status = api.update_with_media(filename,tweet)

# Facebook AOth
def get_api_facebook(cfg):
	graph = facebook.GraphAPI(cfg['access_token'])
	# Get page token to post as the page. You can skip 
	# the following if you want to post as yourself. 
	resp = graph.get_object('me/accounts')
	page_access_token = None
	for page in resp['data']:
		if page['id'] == cfg['page_id']:
			page_access_token = page['access_token']

	graph = facebook.GraphAPI(page_access_token)
	return graph

# Send to facebook
def sendToFacebook():
	#Values for access
	cfg = {
		"page_id"	: "",
		"access_token"	: ""
	}
	api = get_api_facebook(cfg)
	albumid = "fill_with_album_id"
	api.put_photo(image=open(filename,"rb"),caption="caption_for_the_photo", album_path=albumid + "/photos")
	# Use this without album
	#api.put_photo(image=open(filename,"rb"),caption="Estamos na Mini MakerFaire Castelo Branco @makerfairecb #makerfaire #makerfairecb #minimakerfairecb #minimakerfaire")

# Watermark
def addWaterMark():
	# size of watermark to add
	# Remember - should be a small image - change dimentions here
	size_w = 340
	size_h = 145
	# load watermark
	img_watermark = Image.open('<water_to_put_on_image')
	# load image taken
	img_orig = Image.open(filename)
	
	# Perform calculations for the image size
	img_w, img_h = img_orig.size
	# the 20 is a margin from the edge of W and H
	def_w = (img_w - 20) - size_w
	def_h = (img_h - 20) - size_h
	img_orig.paste(img_watermark, (def_w, def_h), img_watermark)
	img_orig.save(filename)
	#img_orig.show()

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

# Blink take picture LED while count down
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

# Blink postSNLed while posting to social networks
def blinkPosting(stop_event):
	# Start 
	while (not stop_event.is_set()):
		print "off"		
		GPIO.output(postSNLed,False)
		sleep(0.5)
		print "on"	
		GPIO.output(postSNLed,True)
		sleep(0.5)
	

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

# Resize picture
def resizeThumbnail(imgName):
	# Where going to use the same name for the resized picture
	img_t = Image.open (filename)
	img_t = img_t.resize((1024,768), PIL.Image.ANTIALIAS)
	# save the resized
	img_t.save(filename_t)

# Display a preview on layer 1
# Picture taken
def displayPreview(imgName):
	# Since the PIL image show is a crapp
	# we use the overlay from the camera to display
	# the preview

	# Since the picture is full resolution but monitor is crap
	# Show the resized picture
	# It's separated because one can, when using a new monitor
	# With more resolution, just coment the resizing bit
	# and no need to change code
	img = Image.open(imgName)
	padding = Image.new('RGB', (
		((img.size[0] + 31) // 32) * 32,
		((img.size[1] + 15) // 16) * 16,
	))
	padding.paste(img, (0,0))
	ov = camera.add_overlay(padding.tostring(), size=img.size)
	ov.layer = 1


# Display a preview on layer 3
# This overlay is the social networks icons
def displayPreview3(imgName):
	# Since the PIL image show is a crapp
	# we use the overlay from the camera to display
	# the preview

	img = Image.open(imgName)
	padding = Image.new('RGB', (
		((img.size[0] + 31) // 32) * 32,
		((img.size[1] + 15) // 16) * 16,
	))
	padding.paste(img, (0,0))
	ov = camera.add_overlay(padding.tostring(), size=img.size)
	ov.alpha = 150
	ov.layer = 3
	return ov

# Function overlaySocialNetwork
def overlaysn():
	imgsn = Image.open('SelectOption.png')
	# Create Overlay
	pad = Image.new('RGB',(
		((imgsn.size[0] + 31) // 32) * 32,
                ((imgsn.size[1] + 15) // 16) * 16,
        ))

	# Paste the overlay
	pad.paste(imgsn, (0,0))
	ov = camera.add_overlay(pad.tostring(), size=imgsn.size)
	ov.alpha = 100
	ov.layer = 3	
	return ov

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

# Main function
# Clear screen
tmp = sp.call('clear',shell=True)
camera = picamera.PiCamera()
# Monitor only displays (and framebuffer) is 1024x768
# camera.resolution = (2592,1944)
# camera.resolution = (1920,1080)
camera.resolution = (1024,768)
#camera.resolution = (1280,720)
#camera.resolution = (1280,1024)
camera.framerate = 24
camera.brightness = 55
camera.sharpness = 0
camera.contrast = 0
#camera.exposure_compensation = 0
#camera.exposure_mode = 'auto'
#camera.meter_mode = 'average'

# Testing here
while (True):
	try:
		camera.start_preview()
		#Show LED Only for Take Picture
		onlyTakePicLed()
		# Wait for button to take Picture
		GPIO.wait_for_edge(takeButton,GPIO.FALLING)
		# Start a thread to count with the LEDs while the images are shown
		# Probably could be used in the overlayCounter function,
		# because it also as timers to show the pictures, but the led effects would not
		# be the same
		thread.start_new_thread ( countingTimerPicture,() )

		# Show the pictures overlay in the camera picture
		overlayCounter()
		# Show all LEDS while taking the picture
		showAllLeds()

		# Define a filename and path
		filename = "fotos/%s.jpg" % (time.strftime("%G%m%d%H%M%S"))
		# camera.capture('pushTesting.jpg')
		camera.capture(filename)
		camera.stop_preview()

		#display image
		# Resize and display the resized one
		#filename_t = "fotos/resized_t.jpg"
		# resizeThumbnail(filename)
		displayPreview(filename)
		# Show overlay
		oo = overlaysn()
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
				camera.remove_overlay(oo)
				GPIO.output(cancelButtonLed,False)
				o = displayPreview3('Aenviar.png')
				#print "Social Networks Button"
				# add watermark
				# Only add watermark if sending to social networks
				addWaterMark()
				sendToTwitter()
				sendToFacebook()
				camera.remove_overlay(o)
				break
			if GPIO.event_detected(cancelButton):
				#print "Canceled"
				camera.remove_overlay(oo)
				break

		# reset GPIOS
		GPIO.remove_event_detect(socialNetworkButton)
		GPIO.remove_event_detect(cancelButton)
		GPIO.remove_event_detect(takeButton)
		camera.stop_preview()
	except KeyboardInterrupt:
		print ("Exited...")
		#offLeds()
		GPIO.cleanup()

