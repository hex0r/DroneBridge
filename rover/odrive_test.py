#!/usr/bin/python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

from __future__ import print_function
from odriveRobot import odriveRobot
from gamePad import GamePad
from differentialDrive import diffDrive
from sbusInput import  sbusPad
from dbRc import DbRC
import time
import math


drive = odriveRobot(serial="206139864D4D") # Initializing odrive for Differential drives
input = DbRC(shm="db_rc_values_t")
#Ginput = GamePad('Sony PLAYSTATION(R)3 Controller')
#Ginput = GamePad('SHANWAN PS3 GamePad')
#Sinput = sbusPad('/dev/ttyUSB0')


t0 = time.monotonic()
while True:
    #drive.setSpeed((20.0 * math.sin((time.monotonic() - t0)*2)))
    drive.setSpeed(input.getSpeed()*0.5)
    #print(str(input.getSpeed()))
    time.sleep(0.1)

# print("goto " + str(int(setpoint)))
#    my_drive.axis0.watchdog_feed()
#    my_drive.axis0.controller.input_vel  = setpoint
# time.sleep(0.01)
# Some more things you can try:

# Write to a read-only property:
#my_drive.vbus_voltage = 11.0  # fails with `AttributeError: can't set attribute`

# Assign an incompatible value:
#my_drive.motor0.pos_setpoint = "I like trains"  # fails with `ValueError: could not convert string to float
