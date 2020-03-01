#!/usr/bin/env python
import time
import picamera

camera = picamera.PiCamera()
camera.resolution = (1920,1080)
while not raw_input():
	camera.start_preview()
camera.capture('testing.jpg')

