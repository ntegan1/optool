#!/usr/bin/env python3
import os

from tools.lib.route import SegmentName
from selfdrive.loggerd.uploader import listdir_by_creation

def is_valid_segment(root, segment):
  try:
    segment_to_segment_name(root, segment)
    return True
  except AssertionError:
    return False

def segment_to_segment_name(data_dir, segment):
  fake_dongle = "ffffffffffffffff"
  return SegmentName(str(os.path.join(data_dir, fake_dongle + "|" + segment)))

def all_segment_names(root):
  segments = []
  for segment in listdir_by_creation(root):
    try:
      segments.append(segment_to_segment_name(root, segment))
    except AssertionError:
      pass
  return segments

def all_routes(root):
  segment_names = all_segment_names(root)
  route_names = [segment_name.route_name for segment_name in segment_names]
  route_times = [route_name.time_str for route_name in route_names]
  unique_routes = list(set(route_times))
  return unique_routes

def segments_in_route(root, route):
  segment_names = [segment_name for segment_name in all_segment_names(root) if segment_name.time_str == route]
  segments = [segment_name.time_str + "--" + str(segment_name.segment_num) for segment_name in segment_names]
  return segments

