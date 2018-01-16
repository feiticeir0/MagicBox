import picamera
from PIL import Image
from time import sleep

with picamera.PiCamera() as camera:
	camera.resolution = (1920,1080)
	camera.framerate = 24
	camera.start_preview()

	# load image
	img = Image.open('1.png')
	
	# create
	pad = Image.new('RGB', (
		((img.size[0] + 31) // 32) * 32,
		((img.size[1] + 15) // 16) * 16,
		))

	pad.paste(img, (0,0))


	o = camera.add_overlay(pad.tostring(), size=img.size)

	o.alpha = 128
	o.layer = 3

	while True:
		sleep(1)

