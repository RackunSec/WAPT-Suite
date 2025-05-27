#!/usr/bin/env python3
## SSRF-Lure Server
## 2025 Douglas@RedSiege.com
##  - Catch incoming SSRF requests and review all data
## 
import http.server
from sys import argv,exit ## Simple System stuff
import urllib.parse as urlparse ## For HTTP GET parameters
import socket ## Socket Errors

## Handle HTTP POST requests:
class MyPOSTHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        ##
        print("[i] Incoming request from {}".format(self.client_address[0]))
        post_data = self.rfile.read(int(self.headers['Content-Length']))
        print("[i] Incoming request headers:")
        print(self.headers)

        ## Now we send back a response to the SSRF:
        self.send_response(200) ## Ensure the server thinks the request was successful
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        ## Get HTTP response data:
        response_data = {'message': 'POST request received', 'data': post_data.decode('utf-8')}
        print("[i] HTTP POST data: ")
        print(post_data.decode('utf-8'))
        print("") ## Simple newline

## Handle HTTP GET requests
class MyGETHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        ## 
        print("[i] Incoming request from {}".format(self.client_address[0]))
        print("[i] Incoming request headers:")
        print(self.headers)

        ## Now we send back a response to the SSRF:
        self.send_response(200) ## Ensure the server thinks the request was successful
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        ## Get HTTP GET parameters:
        parsed_url = urlparse.urlparse(self.path)
        query_params = urlparse.parse_qs(parsed_url.query)
        print("[i] HTTP GET data: ")
        for param in query_params:
            print(" {} = {} ".format(param,query_params[param]))
        print("") ## Simple newline

## How do we use this program?
def usage():
    print("""
 SSRF-Lure
 2025 @RackunSec
 
 Usage: 
   -P (Local port to listen on)
   -L (Local IP to listen on; "all" also accepted)
   -M (HTTP method GET/POST supported)

 Example:
   python3 ssrf-lure.py -M POST -L 127.0.0.1 -P 8080 
    """)
    exit(1) ## Error out

if __name__ == '__main__':
    ## Configure the server:
    if "-M" not in argv or "-L" not in argv or "-P" not in argv:
        usage()
    else:
        local_server = argv[argv.index("-L")+1]
        local_port = int(argv[argv.index("-P")+1])
        http_method = argv[argv.index("-M")+1]
        if local_server == "all": local_server = '' ## Rewrite it
        server_address = (local_server, local_port)
        ## Is this a GET resquest server?
        if http_method == "GET":
            try: ## Handle errors, most-likely mistyped IP address:
                httpd = http.server.HTTPServer(server_address, MyGETHandler)
            except socket.error as e:
                print("[!] SSRF-Lure GET server failed to start! ")
                print(e)
                exit(1)
        ## Is this a POST request server?
        elif http_method == "POST":
            try: ## Handle errors, most-likely mistyped IP address:
                httpd = http.server.HTTPServer(server_address, MyPOSTHandler)
            except socket.error as e:
                print("[!] SSRF-Lure POST server failed to start! ")
                print(e)
                exit(1)               
        else: ## Only supports a few methods for now.
            usage()
        print("[i] SSRF-Lure server running at \"{}\" on port {} ... ".format(local_server,local_port))
        print("[i] CTRL+C to quit")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Stopping SSRF-Lure server ... ")
            exit(1)
        except Exception as e:
            print("[!] SSRF-Lure failed !! ")
            print(e)
            exit(1)
