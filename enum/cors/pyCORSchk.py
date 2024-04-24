#!/usr/bin/env python3
## CORS Header Check
## 2022 @RackunSec
import sys ## exit() and argv
import requests ## HTTP requests
import urllib3 ## Used to weed out the SSL/TLS warnings
urllib3.disable_warnings()

def usage(msg):
    print(f"Error: {msg}\n")
    print("Usage: python3 pyCORSchk.py (URI)")
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        usage("No arguments.")
    else: ## OKAY
        headers = {
            "Origin":"**http://www.kfjasdlsdklfjsdf.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
        }
        uri = sys.argv[1]
        response = requests.get(uri,headers=headers,verify=False)
        #print(response.headers) ## DEBUG
        if "Access-Control-Allow-Origin" in response.headers:
            if response.headers['Access-Control-Allow-Origin']=="*":
                print(f"\n[!] Server has an insecure CORS setting as 'Access-Control-Allow-Origin: *'\n")
            elif "kfjasdlsdklfjsdf" in response.headers['Access-Control-Allow-Origin']:
                print(f"\n[!] Reflected value of 'Origin' in response!\n")
            ## Now we just print it:
            print(f"[i] Access-Control-Allow-Origin is set to: {response.headers['Access-Control-Allow-Origin']}")
            if "Access-Control-Max-Age" in response.headers:
                print(f"[i] Access-Control-Max-Age is set to: {response.headers['Access-Control-Max-Age ']}")
            if "Access-Control-Expose-Headers" in response.headers:
                print(f"[i] Access-Control-Expose-Headers is set to: {response.headers['Access-Control-Expose-Headers']}")
        else:
            print("[!] No Access-Control-Allow-Origin HTTP Respose Header Observed.")

if __name__ == "__main__":
    main()
