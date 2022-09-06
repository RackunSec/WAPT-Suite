#!/usr/bin/env python3
## 2022 Douglas Berdeaux (@RackunSec)
## HTTP Secure Header Scanner:
##   Analyzes HTTP response headers for missing security header values
##
## Http class
##
import requests
from classes.Style import Style
from classes.Headers import HeaderDB
class Http:
    def __init__(self,darkmode):
        self.headers = { # Used for making HTTP requests
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
        }
        self._style = Style(darkmode) # Create UI object
        self.darkmode = darkmode
    def get_url(self,url,args):
        print("")
        self._style.ok(f"Analyzing URL: {url}")
        try:
            requests.packages.urllib3.disable_warnings() # This is stupid and should not have to exist.
            req_data = requests.get(url,verify=False)  ## Ignore the cert if it has issues.
            headers = req_data.headers.items()  ## Headers is a dict
            headerdb = HeaderDB(self.darkmode)
            headerdb.analyze_headers(headers,args)
        except Exception as e:
            self._style.fail(f"ERROR Accessing URL: {e}")

        print("") ## done.
