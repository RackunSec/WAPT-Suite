#!/usr/bin/env
# Scrape a Page and Spit Out Unique Word List for Enumeration
# I whipped this up in a pinch when CeWL was giving me problems.
# 2022 - @RackunSec
import requests
import sys
import re
def usage():
    print("Usage: python3 wwwlist.py (URI) | tee file.txt")
    sys.exit()
if(len(sys.argv)!=2):
    usage()
else:
    unique_words = [] # Empty list
    uri = sys.argv[1] # Argument URI
    if re.match(r"^http(s)?:.*",uri):
        # here I set the User Agent for the Requests:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"}
        #print(f"[i] Scraping URI: {uri}") # DEBUG
        try:
            req_data = requests.get(uri,headers=headers)  ## Make the HTTP request and get the data
        except:
            print(f"[!] Could not access {uri}")
            sys.exit()
        #print(html)
        for i,line in enumerate(req_data.iter_lines()):
            decoded = line.decode("utf-8")
            line_scrubbed = re.sub(r"<[^>]+>","",decoded) # Delete out all HTML tags
            line_scrubbed = re.sub(r"^\s+","",line_scrubbed) # Remove all prepended white space
            line_scrubbed = re.sub(r"[^A-Za-z0-9_ /-]","",line_scrubbed) # Remove Evrything that is not a word character ("_-" is okay)
            line_array = line_scrubbed.split()
            for line_item in line_array:
                if not re.match(r"^$",line_item) and len(line_item)!=1 and line_item not in unique_words: # remove blank lines and such
                    unique_words.append(line_item)
        unique_words.sort()
        for word in unique_words:
            print(word)
    else:
        print(f"[!] Not a Valid URI: {uri}")
        usage()
