#!/usr/bin/env python3


import evdev
import threading
import time

# Initialize globals
speed = 0
turn = 0

class GamepadThread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
        self.gamepad = None
        self.driveSpeed=0
        self.driveTurn =0


    def discoverGamepad(self):
        print("Finding ps3 controller...")
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for device in devices:
            print(device.name)
                #if device.name == 'Sony PLAYSTATION(R)3 Controller':
            if device.name == self.name:
                print("Found controller: " + str(device.name))
                #ps3dev = device.fn
                ps3dev = "/dev/input/js0"
                print("ps3 dev: " + str(device.fn))
                return evdev.InputDevice(ps3dev)
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
                print("Wait for GamePad device")
                while self.gamepad is  None:
                    self.gamepad = self.discoverGamepad()
                    time.sleep(1)
    #        while running:
                while True:

                    for event in self.gamepad.read_loop():   #this loops infinitely
                        print("typ" + str(event.type)+ " code " + str(event.code) + " value " + str(event.value))
                        if event.type == 3:             #A stick is moved
                            if event.code == 4:         #Y axis on right stick
                                self.driveSpeed = self.scale_stick(event.value)
                            if event.code == 3:         #X axis on right stick
                                self.driveTurn = self.scale_stick(event.value)

                        if event.type == 1 and event.code == 304 and event.value == 1:
                            print("X button is pressed. Stopping.")
                            break
            except OSError as exception:
                    print("Lost connection Gamepad start new")
                    self.exceptionClean()
                    time.sleep(1)
                    pass

class GamePad(GamepadThread):

    def __init__(self, name):
        super(GamePad, self).__init__(name)
        self.name = name
        ## Initializing ##
        #game_thread = GamepadThread(self.name) # error

        self.setDaemon(True)
        self.start()

    def getSpeed(self):
        return self.driveSpeed
