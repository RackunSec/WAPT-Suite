#!/usr/bin/env python3
## CORS Header Check
## 2022 @RackunSec
import sys ## exit() and argv
import requests ## HTTP requests
import urllib3 ## Used to weed out the SSL/TLS warnings
from re import search as research ## Regexp
urllib3.disable_warnings() ## Ugh, noisy.

def usage(msg):
    print(f"Error: {msg}\n")
    print("Usage: python3 pyCORSchk.py (URI)")
    sys.exit(1)

def banner():
    print(
        """
        -=|[[[ CORS CHECK ]]]|=-

--- Tool Setup:""")
          

def main():
    if len(sys.argv) == 1:
        usage("No arguments.")
    else: ## OKAY
        headers = {
            "Origin":"http://www.kfjasdlsdklfjsdf.com",
            ##"Access-Control-Request-Method":"GET", ## Thsi is for an OPTIONS request
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
        }

        uri_check = False
        ## just grab the URI from any parameter order:
        for arg in sys.argv:
            if research("^http",arg):
                uri = arg
                uri_check = True
        if not uri_check:
            usage("[!] Please provide at least one URL.")
        else:
            banner()
            ## Are we using Burp Suite?
            print(" [t] Target: {}".format(uri))
            if "--burp" in sys.argv:
                print(" [t] Using Burp Proxy at 127.0.0.1:8080")
                proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"} ## PROXY THROUGH BURP
                response = requests.get(uri,headers=headers,verify=False,proxies=proxies) ## PROXY THROUGH BURP
            else: ## No Burp Suite
                response = requests.get(uri,headers=headers,verify=False)
            #print(response.headers) ## DEBUG
            print("\n--- HTTP Response Analysis:")
            ## CHECK: ACAO
            if "Access-Control-Allow-Origin" in response.headers:
                if response.headers['Access-Control-Allow-Origin']=="*":
                    print(f"\n [!] Server has an insecure CORS setting as 'Access-Control-Allow-Origin: *'\n")
                elif "kfjasdlsdklfjsdf" in response.headers['Access-Control-Allow-Origin']:
                    print(f"\n [!] Reflected value of 'Origin' in response!\n")
                ## Now we just print it:
                print(f" [i] Access-Control-Allow-Origin is set to: {response.headers['Access-Control-Allow-Origin']}")
                if "Access-Control-Max-Age" in response.headers:
                    print(f" [i] Access-Control-Max-Age is set to: {response.headers['Access-Control-Max-Age ']}")
                if "Access-Control-Expose-Headers" in response.headers:
                    print(f" [i] Access-Control-Expose-Headers is set to: {response.headers['Access-Control-Expose-Headers']}")
            else:
                print(" [x] No Access-Control-Allow-Origin HTTP response header observed.")
                #print(response.headers) ## DEBUG

            ## CHECK ACAC:
            if "Access-Control-Allow-Credentials" in response.headers:
                print(" [i] Access-Control-Allow-Credentials HTTP header observed as: {}".format(response.headers['Access-Control-Allow-Credentials']))
            else:
                print(" [x] No Access-Control-Allow-Credentials HTTP header observed.")

            ## CHECK COOP:
            if "Cross-Origin-Opener-Policy" in response.headers:
                print(" [i] Cross-Origin-Opener-Policy HTTP header observed as: {}".format(response.headers['Cross-Origin-Opener-Policy']))
            else:
                print(" [x] No Cross-Origin-Opener-Policy HTTP header observed.")

            ## CHECK COEP:
            if "Cross-Origin-Embedder-Policy" in response.headers:
                print(" [i] Cross-Origin-Embedder-Policy HTTP header observed as: ".format(response.headers['Cross-Origin-Embedder-Policy']))
            else:
                print(" [x] No Cross-Origin-Embedder-Policy HTTP header observed.")


if __name__ == "__main__":
    main()
