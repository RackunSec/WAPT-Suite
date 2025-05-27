#!/usr/bin/env python3
# DREDGEON
# 2023/2024 - Douglas McLain Berdeaux
# Scour files for secrets / entropy
#
# CREDIT: Some regexps were used from: 
#   https://securityonline.info/secretfinder-discover-sensitive-data-in-javascript-files/?expand_article=1
#
from sys import exit as exit
from sys import argv as argv
from os import path as path
import re

def banner():
    print("""
    ____________ ___________ _____  _____ _____ _   _ 
    |  _  \ ___ \  ___|  _  \  __ \|  ___|  _  | \ | |
    | | | | |_/ / |__ | | | | |  \/| |__ | | | |  \| |
    | | | |    /|  __|| | | | | __ |  __|| | | | . ` |
    | |/ /| |\ \| |___| |/ /| |_\ \| |___\ \_/ / |\  |
    |___/ \_| \_\____/|___/  \____/\____/ \___/\_| \_/             
       @RackunSec 
        """)

def usage(err):
    print("[!] ERROR: {}\n".format(err))
    print("[?] Usage: python3 dredgeon.py -f filename.extension")
    exit()

## Matching patterns method:
class Dredgeon():
    def __init__(self,filename):
        self.count = 0 # Start at 0
        self.filename = filename
        ## TODO: offload this into an external dictionary file:
        self.dict_words = ["web","librar","global","javascript","java","code","api"
            "refer","docs","varia","update","delete","remove","handle","second","option"
            "template","assign","config","script","browser","html","form","iframe","minute"]
        ## Check the file:
        if path.isfile(filename):
            print("[i] Checking file: {}\n".format(filename))
            with open(filename) as file:
                for line in file:
                    self.do_all_checks(line)
        else:
            usage(err="File \"{}\" does not exist!".format(filename))

    def do_all_checks(self,line): ## This is all of the checking calls:
        self.uuid(line)
        #self.md5(line) ## This is just plain annoying in the output :/
        self.sha256(line)
        self.jwt(line)
        self.jwe(line)
        self.auth_bearer(line)
        self.aws_uid(line)
        self.aws_rid(line)
        self.aws_url(line)
        self.aws_access_key(line)
        self.aws_secret_key(line)
        self.internal_hosts(line)
        self.email_addresses(line)
        self.google_api(line)
        self.google_captcha(line)
        self.facebook_api(line)
        self.basic_auth(line)
        self.priv_key(line)

    def uuid(self,line):
        name = "UUID" ## Update these two lines for each check:
        regexp = re.compile('[A-Fa-f0-9]{8}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{12}')
        bad_word = "00000000"
        ## Additional checks:

        if regexp.findall(line) and bad_word not in regexp.findall(line)[0]:
            self.print_match(name,regexp.findall(line))


## Google:
    def google_api(self,line):
        name = "Google Site Key" ## Update these two lines for each check:
        regexp = re.compile(r'AIza[0-9A-Za-z-_]{35}')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line))

    def google_captcha(self,line):
        name = "Google Captcha Key" ## Fixed to not show false positives, 12/7/23
        regexp = re.compile(r'[^0-9A-Za-z]6L[0-9A-Za-z-_]{38}|^6[0-9a-zA-Z_-]{39}$')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line))

## IAM
    def basic_auth(self,line):
        name = "Basic Auth"
        regexp = re.compile(r'basic\s*[a-zA-Z0-9=:_\+\/-]+')
        if regexp.findall(line) and not self.check_dict_words(regexp.findall(line)[0]):
            self.print_match(name,regexp.findall(line))        


## Encryption:
    def sha256(self,line):
        name = "sha256 hash" ## Update these two lines for each check:
        regexp = re.compile('[^A-Fa-f0-9][A-Fa-f0-9]{64}[^A-Fa-f0-9]')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line))

    def priv_key(self,line):
        name = "Private Key"
        regexp = re.compile(r'-----BEGIN.*PRIVATE.*-----')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line))


    def md5(self,line):
        name = "md5 hash" ## Update these two lines for each check:
        regexp = re.compile('[^A-Fa-f0-9][A-Fa-f0-9]{32}[^A-Fa-f0-9]')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line))

## JSON Web Tokens:
    def jwt(self,line):
        name = "JSON Web Token" ## Update these two lines for each check:
        regexp = re.compile('eyJ[A-Za-z0-9+/]+\.[A-Za-z0-9+/]+\.[A-Za-z0-9+/_-]+[^A-Za-z0-9+/_-]')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line))

    def jwe(self,line):
        name = "JSON Web Encryption" ## Update these two lines for each check:
        regexp = re.compile('eyJ[A-Za-z0-9+/]+\.[A-Za-z0-9+/]+\.[A-Za-z0-9+/]+\.[A-Za-z0-9+/]+\.[A-Za-z0-9+/]+[^A-Za-z0-9+/]')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line))

    def auth_bearer(self,line):
        name = "Authorization Bearer"
        regexp = re.compile(r'bearer\s*[a-zA-Z0-9_\-\.=:_\+\/]+')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line))

## Amazon AWS:
    def aws_uid(self,line):
        name = "AWS User ID" ## Update these two lines for each check:
        regexp = re.compile('[^A-Z]AIDA[A-Z]+')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line))

    def aws_rid(self,line):
        name = "AWS Role ID" ## Update these two lines for each check:
        regexp = re.compile('[^A-Z]AROA[A-Z]+')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line)) 

    def aws_access_key(self,line):
        name = "AWS Access Key" ## Update these two lines for each check:
        regexp = re.compile('[^A-Z]AKIA[A-Z]+')
        if regexp.findall(line) and not self.check_dict_words(regexp.findall(line)[0]):
            self.print_match(name,regexp.findall(line)) 

    def aws_secret_key(self,line):
        name = "AWS Secret Access Key" ## Update these two lines for each check:
        regexp = re.compile('[^A-Za-z0-9+/][A-Za-z0-9+/]{40}[^A-Za-z0-9+/]')
        regexp2 = re.compile('[G-Zg-z]')
        matched_string = regexp.findall(line) 

        if len(matched_string) > 0 and re.search(regexp2,matched_string[0]) and not self.check_dict_words(matched_string[0]):
            self.print_match(name,regexp.findall(line))

    def aws_url(self,line):
        name = "AWS URL" ## Update these two lines for each check:
        regexp = re.compile(r's3\.amazonaws.com[/]+|[a-zA-Z0-9_-]*\.s3\.amazonaws.com')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line))     


## Internal Network Info:
    def internal_hosts(self,line):
        name = "Internal Host" ## Update these two lines for each check:
        regexp = re.compile(r'(https?)?(://)?(localhost|127\.0\.0\.1|10\.[0-9]+\.[0-9]+\.[0-9]+)(:[0-9]+)?(/[A-Za-z0-9_/-]+)?')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line)) 

## Contact Information:
    def email_addresses(self,line):
        name = "Email Address" ## Update these two lines for each check:
        regexp = re.compile('[A-Z0-9a-z_.-]+@[A-Za-z0-9_-]+\.[A-Za-z]+')
        bad_word = "example.com" ## Remove if you want example data
        bad_word2 = "gmail.com" ## Remove if you want to find Gmail addresses
        if regexp.findall(line) and bad_word not in regexp.findall(line)[0].lower() and bad_word2 not in regexp.findall(line)[0].lower():
            self.print_match(name,regexp.findall(line)) 

## Social Media:
    def facebook_api(self,line):
        name = "Facebook API" ## Update these two lines for each check:
        regexp = re.compile(r'EAACEdEose0cBA[0-9A-Za-z]+')
        if regexp.findall(line):
            self.print_match(name,regexp.findall(line)) 




    ## ADD MORE MATCHES HERE. Ensure that they are called by the do_all_checks() method.



    ## DO NOT EDIT BELOW THIS LINE

    def check_dict_words(self,line):
        for word in self.dict_words:
            if word.lower() in line.lower():
                return True
        return False

    def print_match(self,data_type,text):
        if len(text) > 0: ## We have an array:
            final_text = "" ## placeholder
            for match_string in text: # loop over array:
                if type(match_string) is tuple:
                    final_text = ''.join(match_string)
                    print("[!] POSSIBLE {} IDENTIFIED -> {}".format(data_type,final_text))
                else:
                    print("[!] POSSIBLE {} IDENTIFIED -> {}".format(data_type,match_string))
        ## Basic String
        else:
            final_text = text[0]
            print("[!] POSSIBLE {} IDENTIFIED -> {}".format(data_type,text))
        self.count = self.count+1

    def get_count():
        return self.count

## Our main() function:
def main():
    banner() ## Comment me out to not show.
    if len(argv) == 3:
        count = 0 ## How many matches we have found so far
        if "-f" in argv:
            filename = argv[argv.index("-f")+1]
            ## Check if filename is a file:
            dredge = Dredgeon(filename)
            print("\n[i] Dredge completed. {} matches found.".format(dredge.count))

        else:
            usage(err="No arguments provided.")
    else:
        usage(err="No arguments provided.")

if __name__ == "__main__":
	main()
