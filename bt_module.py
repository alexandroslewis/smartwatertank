import serial
import time
import os

if os.path.exists("/dev/rfcomm0") == False:
    print("Device not connected")
    while True:
        if os.path.exists("/dev/rfcomm0"):
            print("Device connected")
            time.sleep(.5)
            break;

ser = serial.Serial("/dev/rfcomm0", timeout=1, baudrate=115000)
ser.flushInput()
ser.flushOutput()        

def awaitBTUserInput():
    while True:
        out = ser.readline().decode()
        if out != "":
            return out
        
def sendMessage(message):
    f = open("/dev/rfcomm0", "w", 1)
    f.write(message)
    f.close()
    time.sleep(.5)