import picamera
from PIL import Image
from time import sleep

with picamera.PiCamera() as camera:
	# camera.resolution = (1920,1080)
	camera.resolution = (1280,1024)
	camera.framerate = 24
	camera.start_preview()

	# load image
#	img = Image.open('1.png')

	# load 
	twitter = Image.open('SelectOption.png')
	
	# create
	pad = Image.new('RGB', (
		((twitter.size[0]+ 31) // 32) * 32,
		((twitter.size[1]+ 15) // 16) * 16,
	))
	pad.paste(twitter, (0,0),twitter)


	o = camera.add_overlay(pad.tostring(), size=twitter.size)

	o.alpha = 128
	o.layer = 3

	while True:
		sleep(1)

