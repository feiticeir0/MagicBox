import picamera
from PIL import Image
from time import sleep

with picamera.PiCamera() as camera:
	camera.resolution = (1920,1080)
	camera.framerate = 24
	camera.start_preview()

	# load image
	img1 = Image.open('3.png')
	img2 = Image.open('2.png')
	img3 = Image.open('1.png')
	# create
	pad = Image.new('RGB', (
		((img1.size[0] + 31) // 32) * 32,
		((img1.size[1] + 15) // 16) * 16,
		))

	pad.paste(img1, (0,0))

	o = camera.add_overlay(pad.tobytes(), size=img1.size)
	o.alpha = 128
	o.layer = 3

	sleep(2)
	
	camera.remove_overlay(o)
	pad.paste(img2, (0,0))
	o = camera.add_overlay(pad.tobytes(), size=img2.size)
	o.alpha = 128
	o.layer = 3

	sleep(2)

	camera.remove_overlay(o)

	pad.paste(img3, (0,0))
	o = camera.add_overlay(pad.tobytes(), size=img3.size)
	o.alpha = 128
	o.layer = 3

	sleep(2)

