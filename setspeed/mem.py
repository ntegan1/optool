#!/usr/bin/env python3

from multiprocessing import shared_memory
import atexit

class Mem:
  __mem = None
  name = "fff"
  size = 2 # just in case i start testing this at same time as maneuver thing
  vinit = 28 # vmax
  def set(self, v):
    #buf[:4] = bytearray([22, 33, 44, 55])
    self.__mem.buf[0] = v
    self.__mem.buf[1] = v < self.vinit and v >= 0
  def overriding(self):
    return bool(self.__mem.buf[1])
  def get(self):
    return self.__mem.buf[0]
  def __create_or_connect(self):
    try:
      self.__mem = shared_memory.SharedMemory(name=self.name, create=True, size=self.size)
    except:
      self.__mem = shared_memory.SharedMemory(name=self.name, create=False, size=self.size)
  def __cleanup(self):
    self.__mem.close()
    if self.__shouldunlink:
      self.__mem.unlink()
  def __init__(self, autounlink=False):
    self.__shouldunlink = autounlink
    self.__create_or_connect()
    #self.set(self.vinit) # todo maybe dont always do this
    atexit.register(self.__cleanup)

def main():
  mem = Mem(autounlink=True)
  mem.set(0)

main()
