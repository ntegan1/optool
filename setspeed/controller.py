#!/usr/bin/env python3

from .mem import Mem
import atexit

## server.py
# gets a speed (0 to 28)
# gets an accel (100 to -100)
# uses controller.py Server class
#   server.update() # maybe return whether is active
#     so server.py knows hwne to reset timeout handler
#   server.reset() when timeout

## controller.py
# utilize mem. and trnaslate it to client reader
#   client
#     return whether rising edge inactive -> active
#     so reset LoC?
#     wait for server class to make the mem.
#     
## mem.py
# make tests

mem_name = "/maneuver"
mem_size = 4
def clip_speed(speed):
  return 0 if speed < 0 else 28 if speed > 28 else speed
def clip_accel(accel):
  return 0 if accel < 0 else 200 if accel > 200 else accel


class Server:
  lastisactive = False
  def update(self, speed, accel):
    """returns whether active for server.py timeout handler"""
    speed = clip_speed(speed)
    accel = clip_accel(accel)

    isactive = speed < 28
    newlyactive = isactive and not self.lastisactive
    self.lastisactive = isactive

    if isactive:
      if newlyactive:
        self.__mem.setbytes(0, 3, bytearray([speed, accel, 1]))
      else:
        self.__mem.setbytes(0, 2, bytearray([speed, accel]))
    else:
      self.__mem.setbytes(0, 2, bytearray([28, 100]))
    return isactive
  def reset(self):
    """reset when server.py timeout"""
    state = bytearray([28, 100, 0, 0])
    self.__mem.set(state)
    self.lastisactive = False
  def __cleanup(self):
    self.__mem.cleanup()
  def __init__(self):
    self.__mem = Mem(mem_name, mem_size, create=True)
    atexit.register(self.__cleanup)

class Client:
  state = None
  def get_newlyactive(self):
    """return if rising edge, and unset the bit to ack to server
       or maybe moreso to itself"""
    yes = bool(self.state[2])
    if yes:
      self.__mem.setbytes(2, 1, bytearray([0]))
      self.state[2] = 0

    return yes
  def get_speed(self):
    return int(self.state[0])
  def get_accel(self, accel_min, accel_max):
    accel = self.state[1]
    if accel >= 100:
      return (float(accel - 100) / 100.) * accel_max
    else:
      return (float(100 - accel) / 100.) * accel_min
  def get_isactive(self):
    return self.get_speed() < 28
  def update(self):
    self.state = self.__mem.get()
  def __cleanup(self):
    self.__mem.cleanup()
  def __init__(self):
    self.__mem = Mem(mem_name, mem_size, create=False)
    self.state = self.__mem.get()
    atexit.register(self.__cleanup)
    # update function to read all mem at once,
    # 
    # isnewOverride so can reset LoC??? / pid?

    # a_target to feed into pid as well as
    # vcruise from this

