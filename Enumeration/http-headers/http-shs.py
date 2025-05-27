#!/usr/bin/env python3
## 2022 Douglas Berdeaux (@RackunSec)
## HTTP Secure Header Scanner:
##   Analyzes HTTP response headers for missing security header values
##
from classes.Style import Style ## To handle UI style stuff
from classes.Http import Http ## To handle HTTP requests
import sys
import re
##
title = "HTTP Secure Header Scanner"
darkmode=True
style = Style(darkmode)
if len(sys.argv)==1:
    style.usage(title)
else:
    ## Grab the URL and check it:
    url = sys.argv[1]
    if not re.match("^[Hh][Tt][Tt][Pp][Ss]?://",url):
        style.fail("URL seems incorrect.")
        sys.exit()
    else: ## We got a good URL:
        http = Http(darkmode)
        http.get_url(url,sys.argv)
