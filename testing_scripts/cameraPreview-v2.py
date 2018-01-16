#!/usr/bin/env python
import time
import picamera
from time import sleep


camera = picamera.PiCamera()
camera.resolution = (1920,1080)
camera.framerate = 24
camera.start_preview()
try:
	while (True):
		sleep(1)
except (KeyboardInterrupt, SystemExit):
	print "Exiting..."
	camera.stop_preview()
