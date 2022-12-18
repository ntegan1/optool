#!/usr/bin/env python3
import os
import time
import threading
from flask import Flask, send_from_directory, Response
from opsetspeed.shminject import Mem

build_dir="/data/openpilot/opsetspeed/build"
static_dir=build_dir + "/static"
allowed_build = ["asset-manifest.json", "favicon.ico", "logo192.png", "logo512.png", "robots.txt"]
app = Flask(__name__, static_folder=static_dir)

mem = Mem()
vmax = 28

@app.route("/")
def a():
  return send_from_directory(build_dir, "index.html")

@app.route("/ping")
def c():
  #response = flask.jsonify({'some': 'data'})
  response = Response("", status=200,)
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

last_send_time = time.monotonic()
@app.route("/control/<y>")
def control(y):
  global last_send_time
  y = int(y)
  if y >= 0 and y <= vmax:
    mem.set(y)
    last_send_time = time.monotonic()
  response = Response("", status=200,)
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

# maybe use this instead
#@app.route('/', defaults={'path': ''})
#@app.route('/<path:path>')
#def catch_all(path):
#    return 'You want path: %s' % path
@app.route("/<path:name>")
def b(name):
  allowed = name in allowed_build
  return send_from_directory(build_dir, name) if allowed else "f"

def handle_timeout():
  while 1:
    this_time = time.monotonic()
    if (last_send_time+1.1) < this_time:
      mem.set(vmax)
      #print("timeout, no web in %.2f s" % (this_time-last_send_time))
    time.sleep(0.1)

def main():
  threading.Thread(target=handle_timeout, daemon=True).start()
  app.run(host="0.0.0.0")

if __name__ == '__main__':
  main()
