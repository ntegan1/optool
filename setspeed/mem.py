#!/usr/bin/env python3

from multiprocessing import shared_memory
import atexit

class Mem:
  __mem = None
  def set(self, ba):
    #buf[:4] = bytearray([22, 33, 44, 55])
    self.__mem.buf[:self.size] = ba
  def setbytes(self, offset, num, ba):
    self.__mem.buf[offset:(offset+num)] = ba
  def get(self):
    return self.__mem.buf[:self.size]
  def __create_or_connect(self):
    #if self.__create:
    #  try:
    #    mem = shared_memory.SharedMemory(name=self.name)
    #    mem.close()
    #    mem.unlink()
    #  except:
    #    pass
    self.__mem = shared_memory.SharedMemory(
      name=self.name,
      create=self.__create,
      size=self.size
    )
  def __cleanup(self):
    self.__mem.close()
    return
    if self.__create:
      self.__mem.unlink()
  def __init__(self, name, size, create=False):
    self.name = name
    self.size = size
    self.__create = create
    self.__create_or_connect()
    atexit.register(self.__cleanup)

def main():
  mem = Mem("/f", 4)

#main()
