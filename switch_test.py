import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

BUTTON = 17

GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

input_received = False

while input_received == False:
    input_state = GPIO.input(BUTTON)
    if input_state == 0:
        print("button pressed")
        input_received = True

GPIO.cleanup()