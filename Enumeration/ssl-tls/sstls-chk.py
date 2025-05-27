#!/usr/bin/env python3
## SSL/TLS Certificate Check Tool
## 2022 Douglas Berdeaux (@RackunSec)
##
from classes.Http import Http  ## Http class to get data from URL
from classes.Style import Style  ## My terminal theme
from sys import argv,exit  ## for exit() and arguments
from re import match,sub  ## for regexp

def main():
    title = "SSL/TLS Cert Check"
    darkmode = True
    style = Style(darkmode)
    http = Http(darkmode)
    if len(argv) != 2:
        style.usage(title)
    else:
        target = argv[1]  ## Assigned for readability
        if match("^https",target):
            target = sub("^https:..([^/\?:]+).*",r"\1:443",target)
            style.ok(f"Got URL and parsed target as: {target}")
            http.test_sstls(target)
        elif match("^[^A-Z0-9.-]:[0-9]+$",target):
            style.fail(f"The target seems to be wrong {target}")
            style.fail(f"Target must be in format: host/domain:port. E.g.: example.com:443")
        else:  ## We got a good URI:
            http.test_sstls(target)

if __name__ == "__main__": main()
