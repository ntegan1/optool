#!/usr/bin/env python3

from multiprocessing import resource_tracker, shared_memory

def rt_no_shm():
  #https://stackoverflow.com/questions/64102502/shared-memory-deleted-at-exit

  def fix_register(name, rtype):
    if rtype == "shared_memory":
      return
    return resource_tracker._resource_tracker.register(self, name, rtype)
  resource_tracker.register = fix_register

  def fix_unregister(name, rtype):
    if rtype == "shared_memory":
      return
    return resource_tracker._resource_tracker.unregister(self, name, rtype)
  resource_tracker.unregister = fix_unregister

  if "shared_memory" in resource_tracker._CLEANUP_FUNCS:
    del resource_tracker._CLEANUP_FUNCS["shared_memory"]

class Mem:
  __mem = None
  def set(self, ba):
    #buf[:4] = bytearray([22, 33, 44, 55])
    self.__mem.buf[:self.size] = ba
  def setbytes(self, offset, num, ba):
    self.__mem.buf[offset:(offset+num)] = ba
  def get(self):
    return bytearray(self.__mem.buf[:self.size])
  def __create_or_connect(self):
    #if self.__create:
    #  try:
    #    mem = shared_memory.SharedMemory(name=self.name)
    #    mem.close()
    #    mem.unlink()
    #  except:
    #    pass
    rt_no_shm()
    self.__mem = shared_memory.SharedMemory(
      name=self.name,
      create=self.__create,
      size=self.size
    )
  def cleanup(self):
    rt_no_shm()
    self.__mem.close()
    if self.__create:
      self.__mem.unlink()
    self.__mem = None
  def __init__(self, name, size, create=False):
    self.name = name
    self.size = size
    self.__create = create
    self.__create_or_connect()

def main():
  mem = Mem("/f", 4)

#main()
