#!/usr/bin/env python3
# 2022 pyhttpenum - Whipped this up because EyeWitness was giving me troubles in an engagement
# @RackunSec
import requests # HTTP requests
import sys # arguments
import os # exit, file stuff
import datetime # timespamp
import time # timestamp
import re # Regexp

def usage():
    print("Usage: python3 pyhttpenum.py (URL|File of URLs) (Output File (csv))")
    exit()

# Write Data to a Log File:
def write_log(output_file,data): # Write data to a file
    with open(output_file,"a") as csvfile:
        csvfile.write(data)

# Build the log string from the response object:
def log_string(response,url):
    if "<title>" in response.text:
        comment = re.findall(r'.*<title>([^<]+)<.*',response.text)
        comment = comment[0]
    else: # TODO PUT MORE CHECKS HERE
        comment = ""
    if "Server" in response.headers:
        server = response.headers['Server']
    else:
        server = ""
    if "X-Powered-By" in response.headers:
        xpower = response.headers['X-Powered-By']
    else:
        xpower = ""
    if "Content-Length" in response.headers:
        length = response.headers['Content-Length']
    else:
        length = ""
    if response.next is not None:
        redirect = response.next
    else:
        redirect = ""
    return f"{url},{response.status_code},{server},{xpower},{length},{redirect},{comment}\n"

def main():
    if len(sys.argv)!=3:
        usage()
    else:
        output_file = sys.argv[2] # Output File name
        input_file = sys.argv[1] # Input file name
        if os.path.exists(input_file): # This is a file, use it
            with open(input_file) as file:
                hosts = file.readlines() # read in all lines into array
                hosts = [host.rstrip() for host in hosts] # remove newlines

            for url in hosts:
                requests.packages.urllib3.disable_warnings()  # Supress Warnings
                print(f"[i] Requesting {url}")
                try: # Make our HTTP Request
                    response = requests.get(url, timeout=5)
                    write_log(output_file,log_string(response,url))
                except Exception as e:
                    # TODO ADD MORE CHECKS HERE FOR COMMENT FIELD
                    if "SSLError" in repr(e):
                        try:
                            response = requests.get(url, verify=False,timeout=5)
                            write_log(output_file,log_string(response,url))
                        except Exception as e:
                            print(f"[!] SSLError for {url} {e}")
                    else:
                        print(f"Generic Error: {e}")

            sys.exit() # Done.
        else: # This is just a single URL
            print("Single URL not implemented yet.")
            sys.exit()
if __name__ == "__main__":
    main()
