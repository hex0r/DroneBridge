import numpy as np
import mmap
from posix_ipc import SharedMemory
from ctypes import sizeof, memmove, addressof, create_string_buffer
from time import sleep
from ctypes import Structure, c_uint16, Array
import evdev
import threading
import time


class DbRCThread(threading.Thread):
    def __init__(self,shm):
        threading.Thread.__init__(self)
        self.shm = shm
        self.rc_stable = False
        self.rc_shm = SharedMemory(self.shm)
        self.rcbuffer =0
        self.driveSpeed = 0

    def discoverRC(self):
        print("discoverRC...")
        self.rc_stable = True

    def readRcValues(self):
        shm_buf =mmap.mmap(self.rc_shm.fd, 2*14)
        msg_bytes = shm_buf.read()
        self.rcbuffer = np.frombuffer(np.array(msg_bytes), dtype=np.uint16)


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
        return self.scale(value,(1000,2000),(-100,100))

    def exceptionClean(self):
        self.rc_stable = False


    def run(self):
        while True :        #while True:
            try:
                print("Wait for GamePad device")
                while self.rc_stable is  False:
                    self.discoverRC()
                    time.sleep(1)
    #        while running:
                while True:
                     self.readRcValues()
                     self.driveSpeed = self.scale_stick(self.rcbuffer[1])
                     time.sleep(0.2)

            except OSError as exception:
                    print("RC link got lost try to recover")
                    self.exceptionClean()
                    time.sleep(1)
                    pass

class DbRC(DbRCThread):

    def __init__(self, shm):
        super(DbRC, self).__init__(shm)
        #self.name = name
        ## Initializing ##
        #game_thread = GamepadThread(self.name) # error

        self.setDaemon(True)
        self.start()

    def getSpeed(self):
        return self.driveSpeed
