#!/usr/bin/env python3
from .head import head
from .nav import nav

def site_page_with_nav(page_name, content, scripts=""):
  page = ""
  page += """<html>""" + head()
  page += """<header>
  """
  page += nav(page_name)
  page += """</header>
  """
  page += """<body class="bg-nord0 text-nord5">"""
  page += content
  page += "</body>"
  page += scripts
  page += """</html>"""
  return page

def site_page(content, scripts=""):
  page = ""
  page += """<html>""" + head()
  page += """<body class="bg-nord0 text-nord5">"""
  page += content
  page += "</body>"
  page += scripts
  page += """</html>"""
  return page

  

