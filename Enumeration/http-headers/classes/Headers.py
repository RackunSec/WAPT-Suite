#!/usr/bin/env python3
## 2022 Douglas Berdeaux (@RackunSec)
## HTTP Secure Header Scanner:
##   Analyzes HTTP response headers for missing security header values
##
## Headers class
##
from classes.Style import Style # for my theme
import json # to read findings.json file
class HeaderDB: ## Just a clean way to store these headers
    def __init__(self, darkmode):
        self.darkmode = darkmode
        self._style = Style(self.darkmode)
        self._findings = {"info":0,"low":0,"med":0,"high":0} ##  A simple chart of numbers used in issue_graph(self) below.
        with open("findings.json") as findings_json: ## read in the findings.json file and create "db"
            self._header_db = json.load(findings_json)

    ## Create pretty graph after all is done:
    def issue_graph(self,findings):
        self._total = 0 # count the findings
        self._mod = 4 # making the bars longer
        self._style.header("Issues Graph")
        for k,v in findings.items():
            color = self._style.YLLBG # default value
            if k=="med": # change if medium
                color = self._style.ORANBG
            elif k=="high": # change if high
                color = self._style.REDBG
            elif k=="info": # change if info
                color = self._style.BLUEBG
            if v > 0: # Do not print empty bars:
                for i in range(v*self._mod):
                    if(i==0):
                        print(f" {k}:\t{color}{self._style.BLK}{v}",end="")
                    else:
                        print(f"{color} ",end="")
                    self._total = self._total + 1 # increment for later:
                print(f"{self._style.RST}\n") # newline after earch bar.
            else:
                print(f" {k}: ")
        if self._total>1:
            print(f"\n {self._style.info()} Total issues found: {self._style.parens(str(self._total/self._mod)+f'/{len(self._header_db)}')}")
        elif self._total==1:
            print(f" {self._style.info()} One issue found: {self._style.parens(self._total)}")
        else:
            ok(f"No issues found.")

    ## Analyze Headers against the HeadersDB Database:
    def analyze_headers(self,headers,args):
        header_list = {}
        for k,v in headers:
            header_list[k.lower()]=v.lower() # make evrything lowercase
            if "--verbose" in args:
                print(f" {self._style.brackets(k)}: {self._style.CMNT}{v}{self._style.RST}")
            ## Do some server checks:
            if k.lower() == "server" and v.lower() == "cloudflare":
                print(f" {self._style.warn()}Cloudflare detected.{self._style.RST}")
            elif k.lower() == "server":  ## Print the server info anyways.
                print(f" {self._style.brackets('Server')} {v}")
        self._style.header("Header Analysis")  ## print a nice header to separate the data.
        for k in self._header_db.keys():  ## loop over keys in DB
            if k.lower() in header_list.keys():  ## does db key exist in list we made from response headers?
                self._style.ok(f"{k} Discovered")
                ## Do some crit_directives checks here and produce warnings:
                if header_list[k.lower()] in self._header_db[k]['crit_directives']:
                    print(f" {self._style.warn()}Insecure directive discovered for {k}: {header_list[k.lower()]}")
                    self._findings[self._header_db[k]['risk']] = self._findings[self._header_db[k]['risk']] + 1
            else: ## nested JSON:
                self._style.fail(f"\"{k}\" HTTP header missing:") # Calculate the Risk and show color:
                if self._header_db[k]['risk']=="low":
                    color = self._style.YLL
                    self._findings['low']=self._findings['low']+1
                if self._header_db[k]['risk']=="med":
                    color = self._style.ORAN
                    self._findings['med']=self._findings['med']+1
                if self._header_db[k]['risk']=="high":
                    color = self._style.RED
                    self._findings['high']=self._findings['high']+1
                if self._header_db[k]['risk']=="info":
                    color = self._style.BLUE
                    self._findings['info']=self._findings['info']+1
                print(f" {self._style.arrow()} {self._style.brackets('Alias')}: {self._style.CMNT}{self._header_db[k]['alias']}{self._style.RST}")
                print(f" {self._style.arrow()} {self._style.brackets('Risk')}: {color}{self._header_db[k]['risk']}{self._style.RST}")
                for ref in self._header_db[k]['refs']:
                    print(f" {self._style.arrow()} {self._style.brackets('Reference')}:{self._style.CMNT} {ref}{self._style.RST}")
                print(f" {self._style.arrow()} {self._style.brackets('Description')}:{self._style.CMNT} {self._header_db[k]['desc']}{self._style.RST}")
                print(f" {self._style.arrow()} {self._style.brackets('Header Directives')}: {self._style.CMNT}{self._header_db[k]['directives']}{self._style.RST}")
                print(f" {self._style.arrow()} {self._style.brackets('Recommendation')}: {self._style.CMNT}{self._header_db[k]['recommendation']}{self._style.RST}\n")

        self.issue_graph(self._findings)
