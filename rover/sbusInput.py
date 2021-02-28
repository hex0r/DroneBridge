#!/usr/bin/env python3


import evdev
import threading
import time
import sbus
from sbus.rx import SBUSReceiver
from sbus.rx import SBUSReceiver

# Initialize globals
speed = 0
turn = 0

class SbusThread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
        self.sbus = None
        self.driveSpeed=0
        self.driveTurn =0


    def discoverSbus(self):
        print("Finding FTDI Serial")
        sbus = SBUSReceiver(self.name)
        if sbus is not None :
            print("Found FTDI : " + str(self.name))
            return sbus
        else:
            return None

    ## Some helpers ##
    def scale(self,val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.

        val: float or int
        src: tuple
        dst: tuple

        example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
        """
        return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

    def scale_stick(self, value):
        return self.scale(value,(0,255),(-100,100))

    def exceptionClean(self):
        self.gamepad = None
        self.driveSpeed=0
        self.driveTurn =0

    def run(self):
        while True :        #while True:
            try:
                print("Wait for Sbus Device")
                while self.sbus is  None:
                    self.sbus = self.discoverSbus()
                    time.sleep(1)
    #        while running:
                while True:
                    frame = SBUSReceiver.get_frame(self.sbus)
                    print(frame)

            except OSError as exception:
                    print("Lost connection SBUS start new")
                    self.exceptionClean()
                    time.sleep(1)
                    pass

class sbusPad(SbusThread):

    def __init__(self, name):
        super(sbusPad, self).__init__(name)
        self.name = name


        self.setDaemon(True)
        self.start()

    def getSpeed(self):
        return self.driveSpeed
