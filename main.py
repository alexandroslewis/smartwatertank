import os
import csv
from datetime import datetime
import time
import math
from setup_gpio import *

if os.path.exists("calibration_data.txt") == False:
    f = open("calibration_data.txt", "w")
    f.write("8 19 2 115 ")
    print("Please empty tank and press button to continue") # text alert
    awaitUserInput()
    time.sleep(.5)
    print("Calibrating empty water tank") # text alert
    empty_distance = getDistance()
    f.write("%s " %(empty_distance))
    print("Please fill tank with water and press button to continue") # text alert
    awaitUserInput()
    time.sleep(.5)
    print("Calibrating full water tank") # text alert
    full_distance = getDistance()
    f.write("%s" %(full_distance))
    f.close()

f = open("calibration_data.txt")
(start_hour, stop_hour, total_liters, tank_diameter, tank_empty, tank_full) = f.read().split()
start_hour = int(start_hour)
stop_hour = int(stop_hour)
total_liters = float(total_liters)
tank_diameter = float(tank_diameter)
tank_empty = float(tank_empty)
tank_full = float(tank_full)

def checkWaterLeft(curr):
    percentage_left = (curr - tank_full) / (tank_empty - tank_full)
    while (1 - percentage_left) < .05:
        print("Please fill tank with water and press button to continue") # text message
        awaitUserInput() # maybe these will be replace with text trigger
        time.sleep(.5)
        percentage_left = (getDistance() - tank_full) / (tank_empty - tank_full)
        
def getFileName():
    now = datetime.now()
    return "user_data/%s_%s.csv" %(now.isocalendar()[1], now.year)

def addRecord(date_time):
    file_name = getFileName()
    csvf = open(file_name, "a")
    curr_distance = getDistance()
    checkWaterLeft(curr_distance)
    csvf.write("%s, %s\n" %(date_time, curr_distance))
    csvf.close()
    
def getLastRecord():
    list = []
    file_name = getFileName()
    with open(file_name, newline="") as csvf:
        reader = csv.reader(csvf, delimiter=" ")
        for row in reader:
            list.append(row)
    return list[-1]

if os.path.exists("user_data/*.csv") == False:
    file_name = getFileName()
    csvf = open(file_name, "w")
    csvf.write("date_time, distance_f_water(mm)\n")
    csvf.close()
    init_date_time = datetime.now()
    init_date_time = datetime(init_date_time.year, init_date_time.month, init_date_time.day, init_date_time.hour, init_date_time.minute)
    addRecord(init_date_time)

while True:
    today = datetime.now()
    if datetime.now() > datetime(today.year, today.month, today.day, start_hour) and datetime.now() < datetime(today.year, today.month, today.day, stop_hour):
        if today.minute == 0:
            addRecord(datetime.now())
            last_record = getLastRecord()
            prev = float(last_record[2])
            curr = getDistance()
            difference = prev - curr
            radius = tank_diameter / 2
            total_hours = stop_hour - start_hour
            consume_rate = total_liters / total_hours
            vol_consumed = math.pi * pow(radius, 2) * difference
            liters_consumed = vol_consumed * .000001
            if liters_consumed < consume_rate:
                print("Please drink", round((2 * consume_rate) - liters_consumed, 2), "liters this hour") # need to make this cumulative in case multiple hours are missed. also need to change out for text alert          
            time.sleep(60)
            
cleanUpGPIO()