import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

BUTTON = 17
TRIG = 23
ECHO = 24

GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("Sensor initializing")
time.sleep(2)

def awaitUserInput():
    input_received = False
    while input_received == False:
        input_state = GPIO.input(BUTTON)
        if input_state == 0:
            input_received = True

def getDistance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150
    
    distance = round(distance, 3)
    
    distance = distance * 10 # converting to mm
    
    return distance - 6 # calculate sensor height offset in mm
    
def cleanUpGPIO():
    GPIO.cleanup()
    

    