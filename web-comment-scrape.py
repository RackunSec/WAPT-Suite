#!/usr/bin/env python3
## Web Comment Scrape Tool
## 2022 Douglas Berdeaux (@RackunSec)
##
from classes.Style import Style
from sys import argv
from re import match
from classes.Http import Http

title = "Web Comment Scrape Tool"
style = Style()  ## Get my terminal theme going
http = Http()
if len(argv) != 2: # We need a url
    style.usage(title)
else:
    url = argv[1]  ## We stroe this for readability
    if(match("^[hH][Tt][Tt][Pp][sS]?://.+",url)):
        http.get_dom(url)

    else:  ## Bad URL
        style.fail("URL does not seem correct.")
