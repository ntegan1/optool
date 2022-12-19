#!/usr/bin/env python3
from optool.setspeed.controller import Client


import time


if __name__ == "__main__":
  c = Client()
  c.update()
  print("Active: \t" + ("TRUE" if c.get_isactive() else "FALSE"))
  print("Speed: \t\t" + str(c.get_speed()))
  print("Accel: \t\t" + str(c.get_accel(-100., 100.)))
  if c.get_newlyactive():
    print("NEWLYACTIVE")
    time.sleep(2)
