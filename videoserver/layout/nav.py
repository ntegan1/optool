#!/usr/bin/env python3

def navlink(to, name, active):
  classs = "text-nord5 py-1 px-2"
  classs += " hover:bg-nord5 hover:text-nord0" if not active else " bg-nord10"
  result = ""
  result += """<a href=""" + '"'
  result += to + '"' + """class=""" + '"' + classs + '"' + ">" + name + """</a>
  """
  return result

def nav(page_name):
  links = [
    ["/", "Home"],
    ["/public", "Public"],
  ]
  navleft = ""
  navleft += """<div class="flex items-center">
  """
  for link in links:
    navleft += navlink(link[0], link[1], page_name == link[0])
  navleft += """</div>
  """
  result = ""
  result += """
    <div class="bg-nord1 flex items-center justify-between">
    """ + navleft + """
    </div>
  """
  return result

