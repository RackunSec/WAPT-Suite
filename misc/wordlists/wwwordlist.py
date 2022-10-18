#!/usr/bin/env
# Scrape a Page and Spit Out Unique Word List for Enumeration
# I whipped this up in a pinch when CeWL was giving me problems.
# 2022 - @RackunSec
import requests
import sys
import re
import urllib3 ## Used to weed out the SSL/TLS warnings
urllib3.disable_warnings() ## Disable SSL/TLS issues

class Wwwordlist():
    def __init__(self):
        ## Update this for the user agent:
        self.ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'
        self.unique_words = [] ## Store all unique words - will be printed at the end.
        self.unique_attribs_list = [] ## Store all attributes of HTML tags

    def usage(self): ## Simple Usage
        print("Usage: python3 wwwordlist.py (URI) | tee file.txt")
        sys.exit()

    def word_check(self,word): ## Check word to make sure it's a word:
        if re.match(r'^[^A-Za-z0-9]+$',word) or re.match(r'^$',word) or len(word)<=1:
            ## Things like "..." or "&..;", blank lines, etc
            return False
        else:
            return True
    def validate_uri(self,uri): ## Was a Valid URI/URL given to me?
        if re.match(r"^http(s)?://.*",uri):
            return True
        else:
            self.print_error(f"Not a Valid URI: {uri}")

    def print_error(self,msg): ## Print Errors to the screen and exit.
        print(f"[!] {msg}")
        sys.exit()

    def get_dom(self,uri): ## Get the DOM from the provided URI/URL
        headers = {"User-Agent": self.ua}
        try:
            response_data = requests.get(uri,headers=headers,verify=False)  ## Make the HTTP request and get the data
            self.generate_wordlist(response_data) ## generate the word list from this.
        except:
            print(f"[!] Could not access {uri}")
            sys.exit()

    def generate_wordlist(self,response_data): ## generate and print the actual wordlist
            for i,line in enumerate(response_data.iter_lines()):
                decoded = line.decode("utf-8")
                if re.search(r'<[^=>]+="',decoded): ## We have attributes we can pull out:
                     attribs = decoded.split("=")
                     for attrib in attribs:
                         if re.search(r'"[^"]+"',attrib):
                             attrib_clean = re.sub(r'^[^"]*"([^"]+)".*',r'\1',attrib)
                             if attrib_clean not in self.unique_attribs_list:
                                 if self.word_check(attrib_clean):
                                     self.unique_attribs_list.append(attrib_clean)
                line_scrubbed = re.sub(r"<[^>]+>","",decoded) # Delete out all HTML tags
                line_scrubbed = re.sub(r"^\s+","",line_scrubbed) # Remove all prepended white space
                line_scrubbed = re.sub(r"&[a-z]+;"," ",line_scrubbed) # remove &nbsp; etc
                line_scrubbed = re.sub(r"[^A-Za-z0-9._\s/-]","",line_scrubbed) # Remove Evrything that is not a word character ("_-" is okay)
                if line_scrubbed == "": ## Remove lines that are blank
                    continue
                if "/" in line_scrubbed:
                    line_array = line_scrubbed.split("/")
                    for line_item in line_array:
                        if " " in line_item: # the line had a forward slash AND a space:
                            line_item2 = line_item.split()
                            for word2 in line_item2:
                                if word2 not in self.unique_words: # remove blank lines and such
                                    if self.word_check(word2):
                                        self.unique_words.append(word2)
                        else:
                            if len(line_item)!=1 and line_item not in self.unique_words: # remove blank lines and such
                                if self.word_check(line_item):
                                    self.unique_words.append(line_item)
                else:
                    line_array = line_scrubbed.split() # split by whitespace
                    for line_item in line_array:
                        if line_item not in self.unique_words: # remove blank lines and such
                            if self.word_check(line_item):
                                self.unique_words.append(line_item)
            self.unique_words = self.unique_words + self.unique_attribs_list ## Combine the lists
            self.unique_words.sort() ## Sort the list
            for word in self.unique_words:
                print(word)

def main():
    wwwordlist = Wwwordlist() ## instantiate the object from the class above
    if len(sys.argv)!=2:
        wwwordlist.usage()
    else:
        wwwordlist.validate_uri(sys.argv[1]) ## This will fail if bad URI
        wwwordlist.get_dom(sys.argv[1]) ## do your stuff, wwwordlist!

if __name__ == "__main__":
    main()
