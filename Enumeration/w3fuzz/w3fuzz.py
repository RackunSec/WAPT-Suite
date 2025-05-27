#!/usr/bin/python3
## 2025 - Douglas@RedSiege.com (@RackunSec)
## W3fuzz
## The goal here is to keep dependencies at a minimum
##  specifically 3rd-party deps at constant risk of deprecation
##  All dependencies should remain standard Python built-ins
##
from sys import argv ## App arguments array
from sys import exit ## Leaving the app after error
from re import match as rematch ## Egrep
from re import sub as resub ## Sed
from re import compile as recompile ## Compiling Regexp objects
import requests ## HTTP Requests
from os.path import isfile ## Wordlist path check
import urllib3 ## suppress TLS issues (that's for a different tool, this is just enum)
import multiprocessing ## For speed
from datetime import datetime ## Timestamps

## The W3fuzz Class Blueprint:
class W3fuzz():
    def __init__(self,args):
        self.args=args
        ## All filters are valuer=False by default and 
        #   populated via CLI arguments in self.setup() further below
        self.config = {
            "filters":{
                "s_regex":{"name":"Show Regexp","value":False },
                "s_code":{"name":"Show Status Code","value":False },
                "s_len":{"name":"Show Length","value":False },
                "s_string":{"name":"Show String","value":False },
                "h_regex":{"name":"Hide Regexp","value":False },
                "h_code":{"name":"Hide Status Code","value":False },
                "h_len":{"name":"Hide Length","value":False },
                "h_string":{"name":"Hide String","value":False }
            },
            "req_count":0 ## Count number of requests made
        }

    ## perform initial setup for scan configuration
    def setup(self): ## Initialize stuff for config object
        if len(self.args)<3: ## we need arguments.
            self.welcome()
            self.usage()
        ## Parse the targets:
        if "-u" in self.args:
            try:
                self.config["target"] = self.args[self.args.index("-u")+1]
                if not rematch(r'^https?://[a-zA-Z0-9.:?&=%/-]+$',self.config["target"]):
                    self.error("URL Not Valid: [{}]".format(self.config["target"]))
            except Exception as e:
                self.error("Error: {}".format(e))
            ## Are we doing POST requests?
            if "-d" in self.args:
                try:
                    self.config["data"]=self.args[self.args.index("-d")+1]
                    self.config["req_type"]="post"
                    data = self.args[self.args.index("-d")+1]
                    type="post"
                except Exception as e:
                    self.error("Could not parse POST data".format(e))
            else:
                self.config["req_type"]="get"
                self.config["data"]=""
            ## HTTP Headers?
            if "-H" in self.args:
                try:
                    self.config["headers"] = self.args[self.args.index("-H")+1]
                except Exception as e:
                    self.error("Could not parse HTTP headers [{}]".format(e))
            else:
                self.config["headers"]=""
        else:
            self.usage()
        ## Parse headers:
        self.config["headers2send"]={} ## This will be sent in request
        if self.config["headers"]!="":
            all_headers=self.config["headers"].split(";")
            for header in all_headers:
                k,v=header.split(":")
                self.config["headers2send"][k]=v

        ## Get the insertion point ("FUZZ"):
        if not rematch(r'.*FUZZ.*',self.config["target"]) and not rematch(r'.*FUZZ.*',self.config["data"]) and not rematch(r'.*FUZZ.*',self.config["headers"]):
            self.error("You must define an insertion point with the word \"FUZZ\"")
        else: ## We have an insertion point:
            if rematch(r'.*FUZZ.*',self.config["target"]):
                self.config["ins_point"]="url"
            elif rematch(r'.*FUZZ.*',self.config["headers"]):
                self.config["ins_point"]="headers"
            elif rematch(r'.*FUZZ.*',self.config["data"]):
                self.config["ins_point"]="data"

        ## Wordlist check:
        if "-w" in self.args:
            ## We have a wordlist!
            try:
                self.config["wordlist"]=self.args[self.args.index("-w")+1]
                if not isfile(self.config["wordlist"]):
                    self.error("Wordlist file may not exist. Please, check the path.")
            except Exception as e:
                self.error("Could not parse wordlist argument: [{}]".format(e))    
        else:
            self.error("You must specify a wordlist")
            
        ## Filtering responses:
        if "-ss" in self.args: ## filter for strings
            try:
                self.config["filters"]["s_string"]["value"]=self.args[self.args.index("-ss")+1]
            except Exception as e:
                self.error("Could not parse string filter: [{}]".format(e))
        if "-sc" in self.args: ## filter for response code
            try:
                self.config["filters"]["s_code"]["value"]=self.args[self.args.index("-sc")+1]
            except Exception as e:
                self.error("Could not parse status code filter: [{}]".format(e))
        if "-sl" in self.args: ## filter for length
            try:
                self.config["filters"]["s_len"]["value"]=self.args[self.args.index("-sl")+1]
            except Exception as e:
                self.error("Could not parse length filter: [{}]".format(e))                
        if "-sr" in self.args: ## filter for regexp
            try:
                self.config["filters"]["s_regex"]["value"]=self.args[self.args.index("-sr")+1]
            except Exception as e:
                self.error("Could not parse regexp filter: [{}]".format(e))
        if "-hc" in self.args: ## Filter OUT HTTP response codes
            try:
                self.config["filters"]["h_code"]["value"]=self.args[self.args.index("-hc")+1]
            except Exception as e:
                self.error("Could not parse status code filter: [{}]".format(e))        
        if "-hl" in self.args: ## Filter OUT HTTP response lengths
            try:
                self.config["filters"]["h_len"]["value"]=self.args[self.args.index("-hl")+1]
            except Exception as e:
                self.error("Could not parse length filter: [{}]".format(e))
        if "-hs" in self.args: ## Filter OUT HTTP responses that contain a user-specified string
            try:
                self.config["filters"]["h_string"]["value"]=self.args[self.args.index("-hs")+1]
            except Exception as e:
                self.error("Could not parse length filter: [{}]".format(e))
        if "-hr" in self.args: ## This doesn't really make sense, since you can use [^ ... ]
            try:
                self.config["filters"]["h_regex"]["value"]=self.args[self.args.index("-hr")+1]
            except Exception as e:
                self.error("Could not parse length filter: [{}]".format(e))
        self.print_config() ## Print config to terminal for screenshots
        self.prep_req() ## Let's start scanning!
        self.wrap_up() ## Print wrap up info

    def wrap_up(self):
        print("\n Total Requests Made in this Session: {} \n".format(self.config["req_count"]))

    ## Pretty print the config for screenshots:
    def print_config(self):
        print(" Scan Configuration:\n -------------------------")
        print(" Target URL: {}".format(self.config["target"]))
        print(" Request Type: {}".format(self.config["req_type"].upper()))
        for filter in self.config["filters"]:
            if self.config["filters"][filter]["value"]: ## Value will ONLY be true if set in code above
                print(" Filter Applied: {} of {}".format(self.config["filters"][filter]["name"],self.config["filters"][filter]["value"]))
        print(" Insertion Point Location: {}".format(self.config["ins_point"].upper()))
        if self.config["headers"]!="":
            print(" Headers: {}".format(self.config["headers"]))
        if self.config["data"]!="":
            print(" POST Data: {}".format(self.config["data"]))
        print(" Wordlist: {}\n\n Scan Began: {} \n".format(self.config["wordlist"],datetime.now()))

    ## Make the requests:
    def prep_req(self): ## config is already in instantiated object
        ## Back these up to avoid clobbering:
        self.config["target_control"]=self.config["target"]
        self.config["data_control"]=self.config["data"]
        self.config["headers_control"]=self.config["headers"]
        ## Print out our table:
        print(" Payload".ljust(20), end = "")
        print("Status".ljust(20), end = "")
        print("Length".ljust(20), end = "")
        print("\n ------------------------------------------------")

        with open(self.config["wordlist"]) as wordlist:
            mprocesses = []
            for word in wordlist:
                esc_word = word.replace('\\','\\\\').strip() ## Attempt to resolve replace issues with "\"
                #print("[i] testing: {}".format(esc_word)) ## DEBUG
                ## insert using re.sub - Data, Headers, or Target URL
                if self.config["ins_point"]=="data":
                    self.config["data"]=resub(r'FUZZ',word.strip(),self.config["data_control"])
                elif self.config["ins_point"]=="url":
                    #self.config["target"]=resub(r'FUZZ',word.strip(),self.config["target_control"])
                    self.config["target"]=self.config["target_control"].replace('FUZZ',esc_word)
                elif self.config["ins_point"]=="headers":
                    self.config["headers"]=resub(r'FUZZ',word.strip(),self.config["headers_control"])
                ## Multiprocessing to speed up the scans:
                self.config["req_count"] = self.config["req_count"]+1 ## Count requests (we do this before multiprocessing)
                mp = multiprocessing.Process(target=self.make_req,args=(esc_word,))
                mprocesses.append(mp) ## Collect the process here for later
                mp.start()
            for process in mprocesses: ## Now we collect all the processes
                process.join() ## and ensure they are done before printing the footer stats.
                #self.make_req(self.config,esc_word) ## DEBUG

    ## Make the HTTP request:
    def make_req(self,word):
        if(self.config["req_type"]=="get"):
            try:
                urllib3.disable_warnings() ## Supress TLS issues as we are not worried about that now.
                response = requests.get(self.config["target"],verify=False,headers=self.config["headers2send"])
            except Exception as e:
                self.error("Something went wrong: [{}]".format(e))
            ## Apply filters
            ## Since one was true, let's apply it using a bunch of return statements:
            if self.config["filters"]["s_regex"]["value"]: ## Filter for reponses with specific pattern in body
                if not rematch(recompile(self.config["filters"]["s_regex"]["value"]),response.text):
                    return ## Didn't match, else continue
            if self.config["filters"]["s_code"]["value"]: ## Filter for specific HTTP response code
                if response.status_code!=int(self.config["filters"]["s_code"]["value"]):
                    return ## Didn't match, else continue
            if self.config["filters"]["s_len"]["value"]: ## Filter for specific HTTP response length
                if response.len(response.text)!=int(self.config["filters"]["s_len"]["value"]):
                    return ## Didn't match, else continue
            if self.config["filters"]["s_string"]["value"]: ## Filter for specific string in HTTP response body
                if self.config["filters"]["s_string"]["value"] not in response.text:
                    return ## Didn't match, else continue
            if self.config["filters"]["h_regex"]["value"]: ## This needs review
                if rematch(recompile(self.config["filters"]["h_regex"]["value"]),response.text):
                    return ## Matched, so skip it (h_.*)
            if self.config["filters"]["h_code"]["value"]: ## Filter out specific HTTP response body lengths
                if response.status_code==int(self.config["filters"]["h_code"]["value"]):
                    return
            if self.config["filters"]["h_len"]["value"]: ## Filter OUT responses that match length in args
                if response.len(response.text)==int(self.config["filters"]["h_len"]["value"]):
                    return
            if self.config["filters"]["h_string"]["value"]:
                if self.config["filters"]["h_string"]["value"] in response.text:
                    return ## Matched, else continue
            ## So, since we didn't return due to fliters, let's proceed:
            print(" {}".format(word).ljust(20), end = "")
            print("{}".format(response.status_code).ljust(20), end = "")
            print("{}".format(len(response.content)).ljust(20))

    ## Welcome message:
    def welcome(self):
        print("""              __       ___                           
            /'__`\   /'___\                          
 __  __  __/\_\L\ \ /\ \__/  __  __  ____    ____    
/\ \/\ \/\ \/_/_\_<_\ \ ,__\/\ \/\ \/\_ ,`\ /\_ ,`\  
\ \ \_/ \_/ \/\ \L\ \\ \ \_/\ \ \_\ \/_/  /_\/_/  /_ 
 \ \___x___/'\ \____/ \ \_\  \ \____/ /\____\ /\____\\
  \/__//__/   \/___/   \/_/   \/___/  \/____/ \/____/             
 
 Web Application Enumeration via Fuzzing
 2025, @RackünSec
          """)

    ## Print usage:
    def usage(self):
        print(""" Usage: 
    -u (TARGET URL)
    -H (HTTP Headers: e.g.: "User-Agent:Mozilla Browser;Authorization:Bearer ...")
    -d (HTTP POST data: e.g.: "id=13&user=administrator&session=true")
    -c (HTTP Cookies, delimited with semicolons)
          
 Filtering:
    -[s/h]c (int): Show/Hide responses that match HTTP code
    -[s/h]l (int): Show/Hide http responses that match HTTP code
    -[s/h]r (regexp): Show/Hide http responses that match Regexp in body
    -[s/h]s (String): Show/Hide http responses that match a string in body
          """)
        exit()

    ## Print errors:
    def error(self,msg):
        print("[!] Error: {}".format(msg))
        exit()

## Init:
if __name__ == "__main__":
    app = W3fuzz(argv)
    app.setup()
