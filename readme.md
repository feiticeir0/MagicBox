# Raspberry PI MagicBox ![MagicBox](https://github.com/feiticeir0/MagicBox/blob/master/MagicBox.jpg)

##### Using a Raspberry PI and the Pi camera, some Big Push Dome buttons.
##### It uses only the framebuffer of the RPi (no X) to present a countdown timer before taking the picture, and if the person likes the picture it can upload it to Facebook or Twitter. 
##### It can also add a watermark to the picture taken (small image in one of the corners) . 

**How does it work?**

When pressing a button, a countdown starts from 3 to 1. After the countdown, a picture is taken (both Big dome push buttons blink). After the picture is taken, it is shown in the monitor and 2 options are given to the user:

	* Upload to facebook and twitter
	* Cancel and try again

Everything is programmed in *Python3* and run without Xorg, just using the Raspberry PI Frame buffer. 

You can watch a small video of the project here: 
https://www.youtube.com/watch?v=V5zME-hghag


## There's an Instructable of this project  
[RaspberryPI Photo Camera - MagicBox](https://www.instructables.com/id/RaspberryPI-Photo-Camera-MagicBox/)



