#!/usr/bin/env python3
import os
import requests
import pickle
mydir = os.path.dirname(os.path.abspath(__file__)) 
pf = mydir + "/" + "dongle.pickle"

def from_date(from_datetime=None):
  #import datetime
  #epoch = datetime.datetime(2021, 7, 7, 1, 2, 1).strftime('%s')
  SINCE_BEGINNING_OF_TIME = "0"
  return SINCE_BEGINNING_OF_TIME
  ## Old bash stuff
  # note it's in epoch MILLIS
  #from_date="$(date_to_epoch_millis 'Wed Jul 24 09:50:03 AM EDT 2022')"
  #from_date="$(date_to_epoch_millis 'Sep 7 08:40:03 PM EDT 2022')"
  #from_date=0
  #function date_to_epoch_millis() {
  #  date_in="${1}"
  #  secs=$(date -d "${date_in}" +%s)
  #  echo $((secs * 1000))
  #}

def comma_request(path):
  jwtenv = os.environ.get("jwt")
  jwt = "" if jwtenv is None else jwtenv
  url = "https://api.commadotai.com/"
  #curl 2>/dev/null -L -H "Authorization: JWT ${jwt}" ${url}/${endpoint}
  headers = {
    "Authorization": "JWT " + jwt,
    'user-agent': 'agnos/0.9.1',
  }
  r = requests.get(url + path, headers=headers)
  return r.json() if r.status_code == 200 else None

class Dongle:
  # Cached segments from which routes can be derived
  segments = None
  # Cached files for each route
  files = None
  def __fetch_cache_files(self):
    if self.files is not None:
      return
    self.files = {}
    d = self.dongle
    for route in self.list_routes():
      reqpath = "v1/route/"
      reqpath += self.dongle + "|" + route + "/files"
      rj = comma_request(reqpath)
      self.files[route] = rj
    #print(rj.keys()) #['cameras', 'dcameras', 'ecameras', 'logs', 'qcameras', 'qlogs']
  def __fetch_cache_segments(self):
    """make the commaapi request"""
    if self.segments is not None:
      return
    d = self.dongle
    fd = from_date()
    reqpath = "v1/devices/"
    reqpath += d + "/"
    reqpath += "segments?from=" + fd
    rj = comma_request(reqpath)
    self.segments = rj
  def list_segments(self):
    """make the request and cache"""
    self.__fetch_cache_segments()
    #request v1/devices/${dong}/segments?from=${from} | jq -r '.[].canonical_name'
    return [s["canonical_name"].rsplit("|")[-1] for s in self.segments]
  def list_routes(self):
    """make the request and cache"""
    self.__fetch_cache_segments()
    #request v1/devices/${dong}/segments?from=${from} | jq -r '.[].canonical_route_name' | uniq
    return list(set([s["canonical_route_name"].rsplit("|")[-1] for s in self.segments]))
  def list_files(self, route):
    """make the request and cache"""
    self.__fetch_cache_segments()
    self.__fetch_cache_files()
    return self.files[route]
  def __init__(self, dongle):
    self.dongle = dongle

def savenew():
  dongle = Dongle("0def4a390f6fe5c0")
  dongle.list_files(dongle.list_routes()[0])
  with open(pf, "w+b") as f:
    f.seek(0)
    f.write(bytes(pickle.dumps(dongle)))
def load():
  dongle = pickle.loads(open(pf, "rb").read())
  return dongle
if __name__ == "__main__":
  #savenew()
  dongle = load()
  route = dongle.list_routes()[0]
  files = dongle.list_files(route)
  print(files["qcameras"])

