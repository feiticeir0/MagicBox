from RPi import GPIO

takeButton = 17
brakeButton = 27
led1 = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(takeButton, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(led1,GPIO.OUT)

#Light led
GPIO.output(led1,True)
# Blocking function
GPIO.wait_for_edge(takeButton,GPIO.FALLING)
GPIO.output(led1,False)
GPIO.cleanup()
