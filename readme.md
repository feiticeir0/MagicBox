#Raspberry PI PhotoBooth#

##### Using a Raspberry PI and the Pi camera, some Big Push Dome buttons.
##### It uses only the framebuffer of the RPi (no X) to present a countdown timer before taking the picture, and if the person likes the picture it can upload it to Facebook or Twitter. 
##### It can also add a watermark to the picture taken (small image in one of the corners) . 

**How does it work?**
When pressing a button, a countdown appears from 3 to 1. After the countdown, a picture is taken (both Big dome push buttons blink). After the picture is taken, it is shown in the monitor and 2 options are given to the user:
	* Upload to facebook and twitter
	* Cancel and try again

Everything is programmed in *Python* and run without Xorg, just using the Raspberry PI Frame buffer. 

To run it, just

**python RPiPhotoBooth.py**

More information on this project ca be found at
https://blog.whatgeek.com.pt/2017/05/raspberry-pi-photo-booth-with-social-networks-sharing

###### Some images of the project ######
![Raspberry PI Photobooth Front]
(http://blog.whatgeek.com.pt/wp-content/uploads/2017/03/IMG_20160607_232200.jpg)


