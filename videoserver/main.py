#!/usr/bin/env python3

from layout import site_page, site_page_with_nav
from util.route import segments_in_route, all_routes, all_segment_names, segment_to_segment_name, is_valid_segment
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
    <div class="flex w-full h-full">
      <video id="video" class="bg-nord1 w-fit h-fit" width="320" height="240" controls autoplay="autoplay">
      </video>
      <div id="drag" class="draggable w-64 h-64 m-8 bg-nord10">
      </div>
    </div>
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
    document.getElementById('drag').DraggableJS();
    document.getElementById('video').DraggableJS();
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
