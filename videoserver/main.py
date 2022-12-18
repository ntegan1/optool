#!/usr/bin/env python3

from layout import site_page, site_page_with_nav
from util.route import segments_in_route, all_routes, all_segment_names, segment_to_segment_name, is_valid_segment
from util.capi import Dongle
from util.ffmpeg import ffmpeg_mp4_concat_wrap_process_builder, ffmpeg_mp4_wrap_process_builder
from flask import Flask, Response, request
#from selfdrive.loggerd.config import ROOT

ROOT = "/home/ntegan/2022_11_22_tomtp/"

app = Flask(__name__,)

@app.route("/full/<cameratype>/<route>")
def full(cameratype, route):
  chunk_size = 1024 * 512 # 5KiB
  #if not is_valid_route(route):
  #  return "invalid route"
  file_name = cameratype + (".ts" if cameratype == "qcamera" else ".hevc")
  vidlist = "|".join(ROOT + "/" + segment + "/" + file_name for segment in segments_in_route(ROOT, route))
  def generate_buffered_stream():
    with ffmpeg_mp4_concat_wrap_process_builder(vidlist, cameratype, chunk_size) as process:
      for chunk in iter(lambda: process.stdout.read(chunk_size), b""):
        yield bytes(chunk)
  return Response(generate_buffered_stream(), status=200, mimetype='video/mp4')

@app.route("/<cameratype>/<segment>")
def fcamera(cameratype, segment):
  if not is_valid_segment(ROOT, segment):
    return "invalid segment"
  file_name = ROOT + "/" + segment + "/" + cameratype + (".ts" if cameratype == "qcamera" else ".hevc")

  return Response(ffmpeg_mp4_wrap_process_builder(file_name).stdout.read(), status=200, mimetype='video/mp4')

@app.route("/<route>")
def route(route):
  if len(route) != 20:
    return "route not found"

  if str(request.query_string) == "b''":
    query_segment = str("0")
    query_type = "qcamera"
  else:
    query_segment = (str(request.query_string).split(","))[0][2:]
    query_type = (str(request.query_string).split(","))[1][:-1]

  links = ""
  segments = ""
  for segment in segments_in_route(ROOT, route):
    links += "<a href='"+route+"?"+segment.split("--")[2]+","+query_type+"'>"+segment+"</a><br>"
    segments += "'"+segment+"',"
  content = """
    <video id="video" width="320" height="240" controls autoplay="autoplay" style="background:black">
    </video>
    <br><br>
    current segment: <span id="currentsegment"></span>
    <br>
    current view: <span id="currentview"></span>
    <br>
    <a download=\""""+route+"-"+ query_type + ".mp4" + """\" href=\"/full/"""+query_type+"""/"""+route+"""\">download full route """ + query_type + """</a>
    <br><br>
    <a href="\\">back to routes</a>
    <br><br>
    <a href=\""""+route+"""?0,qcamera\">qcamera</a> -
    <a href=\""""+route+"""?0,fcamera\">fcamera</a> -
    <a href=\""""+route+"""?0,dcamera\">dcamera</a> -
    <a href=\""""+route+"""?0,ecamera\">ecamera</a>
    <br><br>
    """+links
  scripts="""
    <script>
    var video = document.getElementById('video');
    var tracks = {
      list: ["""+segments+"""],
      index: """+query_segment+""",
      next: function() {
        if (this.index == this.list.length - 1) this.index = 0;
        else {
            this.index += 1;
        }
      },
      play: function() {
        return ( \""""+query_type+"""/" + this.list[this.index] );
      }
    }
    video.addEventListener('ended', function(e) {
      tracks.next();
      video.src = tracks.play();
      document.getElementById("currentsegment").textContent=video.src.split("/")[4];
      document.getElementById("currentview").textContent=video.src.split("/")[3];
      video.load();
      video.play();
    });
    video.src = tracks.play();
    document.getElementById("currentsegment").textContent=video.src.split("/")[4];
    document.getElementById("currentview").textContent=video.src.split("/")[3];
    </script>
"""
  return site_page_with_nav("", content, scripts=scripts)

@app.route("/public/<dongle>/<route>")
def publicdongleroute(dongle, route):
  # return qcams
  #chunk_size = 1024 * 512 # 5KiB
  #file_name = cameratype + (".ts" if cameratype == "qcamera" else ".hevc")
  #vidlist = "|".join(ROOT + "/" + segment + "/" + file_name for segment in segments_in_route(ROOT, route))
  #def generate_buffered_stream():
  #  with ffmpeg_mp4_concat_wrap_process_builder(vidlist, cameratype, chunk_size) as process:
  #    for chunk in iter(lambda: process.stdout.read(chunk_size), b""):
  #      yield bytes(chunk)
  #return Response(generate_buffered_stream(), status=200, mimetype='video/mp4')
  return ""
@app.route("/public", methods=["GET"])
def public():
  args = request.args
  dongle = args.get("dongle")
  inputclass="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

  routelinks = ""
  if dongle is not None:
    try:
      d = Dongle(dongle)
      for r in d.list_routes():
        link = "/public/" + dongle + "/" + r
        routelinks += """
          <a href=""" + '"' + link + '"' + ">" + r + """</a><br>
        """
    except:
      pass
    
  result = ""
  result += """
    <div class="mt-4 ml-4 bg-nord1 p-2 text-nord5 w-fit">
      <h1 class="text-2xl">Public Dongle Search</h1>
      <form action="/public" method="GET">
        <label for="dongle">DongleID</label><br>
        <input name="dongle" title="DongleID is 16 characters" placeholder="ffffaaaabbbbcccc" id="dongle" type="text" class="placeholder:text-nord8 bg-nord3" maxlength="16" pattern="[a-fA-F0-9]{16}" required>
        </input>
        <button type="submit">submit</button>
      </form>
      <h4 class="text-md">e.g. 0def4a390f6fe5c0</h4>
      <br><br>
      <h1 class="text-lg font-bold">Routes</h1>
      """ + routelinks + """
    </div>
  """
  return site_page_with_nav("/public", result)

@app.route("/")
def index():
  result = ""
  for route in all_routes(ROOT):
    result += "<a href='"+route+"'>"+route+"</a><br>"
  return site_page_with_nav("/", result)

def main():
  app.run(host="0.0.0.0", port="8081")

if __name__ == '__main__':
  main()
