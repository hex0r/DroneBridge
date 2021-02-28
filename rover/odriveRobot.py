import odrive
from odrive.enums import *
import odrive.shell
import time


class odriveRobot:
  def __init__(self, serial):

    self.r_serial = serial
    self.discoverOdrive()
    self.configure()

  def USBerror(self):
    print("Device disconnected")
    self.discoverOdrive()
    self.configure()

  def discoverOdrive(self):
    self.my_drive = odrive.find_any(serial_number=self.r_serial)
    self.my_drive.__channel__._channel_broken.subscribe(self.USBerror)

  def configure(self):

    self.my_drive.axis0.config.enable_watchdog = False
    self.my_drive.axis0.clear_errors()
    self.my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    self.my_drive.axis0.config.watchdog_timeout = 0.2
    print("Clear odrive error")


  def setSpeed(self , speed):
    try:
        if self.checkIfAlive():
            self.my_drive.axis0.config.enable_watchdog = True
            self.my_drive.axis0.watchdog_feed()
            self.my_drive.axis0.controller.input_vel = speed
        else: # failue try to recover
            self.bringToLife()
    except:
        print("Something went wrong")
        time.sleep(1)
        self.bringToLife()
        pass


  def checkIfAlive(self):
    # check if odrive is connected
    # check if motors have failures
    if self.my_drive.axis0.error == 0:
        return True
    else:
        return False

  def bringToLife(self):
    # check if odrive is connected
    # check if motors have failures
    print("Reboot odrive")
    self.my_drive.axis0.clear_errors()
    self.my_drive.reboot()
    self.configure()
    return True
