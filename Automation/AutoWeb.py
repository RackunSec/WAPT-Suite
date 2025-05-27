#!/usr/bin/env python
## Autoweb.py - Automate the first day.
## 2022 @RackunSec
##
##
import sys # for arguments
import os # for file stuff
import re # regexp stuff
import subprocess # run commands
import csv # read CSV output from Wfuzz
import configparser # Read the config file and get info

def read_config(ini_file,type,app):
    config = configparser.ConfigParser()
    config.read(ini_file)
    app_path = config.get(type,app,fallback=f"NOT_FOUND")
    if app_path != "NOT_FOUND":
        if(app_path!=""):
            return app_path
        else:
            err(f"{app} not defined in config file: {ini_file}.")
    else:
        err(f"{app} not defined in config file: {ini_file}.")

def say_msg(msg):
    print("[i] "+msg)

def usage(err):
    print(f"[!] Error: {err}")
    print("Usage: python3 AutoWeb.py (LIST OF URIs)")
    sys.exit()

def err(fatal_msg):
    print(f"[!] Fatal: {fatal_msg}")
    sys.exit(1)

def warn(warn_msg):
    print(f"[!] Warning: {warn_msg}")

def run_cmd(cmd,log_path,url,cur_dir):
    path_full = log_path+f"{cmd}.txt" # for the log file (per tool)
    ## SSLScan:
    if cmd == "sslscan": # SSLScan - path defined at top of script
        sslscan_path = read_config(cur_dir+"/Config_AutoWeb.ini","PATHS","SSLSCAN")
        cmd_full = f"{sslscan_path} --no-colour {url} > {path_full}"
        log = open(path_full,"w")
        log.write(f"#####\n##{cmd_full}\n#####\n\n") # log the actual command ran
        log.close() # close it up
        cmd = subprocess.Popen(cmd_full,shell=True)
        cmd.wait() # wait for meeeeee!
    ## Nikto.pl:
    elif cmd == "nikto": # Nikto - path defined at top of script
        nikto_path = read_config(cur_dir+"/Config_AutoWeb.ini","PATHS","NIKTO")
        cmd_full = f"{nikto_path} -h {url}  > {path_full}"
        log = open(path_full,"w")
        log.write(f"#####\n##{cmd_full}\n#####\n\n") # log the actual command ran
        log.close() # close it up
        cmd = subprocess.Popen(cmd_full,shell=True)
        cmd.wait() # wait for meeeeee!
    ## WFuzz (big.txt):
    elif cmd == "wfuzz": # Wfuzz - path defined at top of script
        wfuzz_path = read_config(cur_dir+"/Config_AutoWeb.ini","PATHS","WFUZZ")
        wordlist = read_config(cur_dir+"/Config_AutoWeb.ini","PATHS","WORDLIST")
        cmd_full = f"{wfuzz_path} --hc 404 --hl 0 -f {log_path}wfuzz_big.txt,csv -w {wordlist} {url}/FUZZ > /dev/null"
        cmd = subprocess.Popen(cmd_full,shell=True)
        cmd.wait() # wait for meeeeee!
        log = open(log_path+"wfuzz_big.txt","a") # This needs to append because wfuzz will overwrite anything in the file
        log.write(f"#####\n##{cmd_full}\n#####\n\n") # log the actual command ran
        log.close() # close it up
    ## Http-SHS:
    elif cmd == "http-shs":
        py_web_tools_path = read_config(cur_dir+"/Config_AutoWeb.ini","PATHS","PY_WEB_TOOLS")
        os.chdir(py_web_tools_path+"/enum/http-headers")
        cmd_full = f"python3 http-shs.py {url}  > {path_full}"
        cmd = subprocess.Popen(cmd_full,shell=True)
        cmd.wait()
        os.chdir(cur_dir) # Go back.
    ## Http-Scan:
    elif cmd == "http-scan":
        py_web_tools_path = read_config(cur_dir+"/Config_AutoWeb.ini","PATHS","PY_WEB_TOOLS")
        os.chdir(py_web_tools_path+"/enum/http-scan")
        target_file = f"{log_path}target_url.txt"
        cmd_full = f"python3 pyhttpenum.py {target_file} {log_path}http-scan.txt"
        cmd = subprocess.Popen(cmd_full,shell=True)
        cmd.wait()
        os.chdir(cur_dir) # Go back.
    ## WWWordlist:
    elif cmd == "wwwordlist":
        py_web_tools_path = read_config(cur_dir+"/Config_AutoWeb.ini","PATHS","PY_WEB_TOOLS")
        os.chdir(py_web_tools_path+"/misc/wordlists")
        cmd_full = f"python3 wwwordlist.py {url} > {log_path}wwwordlist.txt"
        cmd = subprocess.Popen(cmd_full,shell=True)
        cmd.wait()
        os.chdir(cur_dir) # Go back.
    ## pyCORSchk:
    elif cmd == "pyCORSchk":
        py_web_tools_path = read_config(cur_dir+"/Config_AutoWeb.ini","PATHS","PY_WEB_TOOLS")
        os.chdir(py_web_tools_path+"/enum/cors")
        cmd_full = f"python3 pyCORSchk.py {url} > {log_path}cors.txt"
        cmd = subprocess.Popen(cmd_full,shell=True)
        cmd.wait()
        os.chdir(cur_dir) # Go back.
    ## Byp4xx.py:
    elif cmd == "byp4xx":
        byp4xx_path = read_config(cur_dir+"/Config_AutoWeb.ini","PATHS","BYP4XX")
        with open(log_path+"wfuzz_big.txt") as wfuzz_csv:
            csvreader = csv.reader(wfuzz_csv)
            os.chdir(byp4xx_path) # go there.
            for row in csvreader:
                try:
                    if int(row[1]) > 399 and int(row[1]) < 404:
                        test_403 = url+row[5]
                        say_msg(f" --> Attacking: {test_403}")
                        cmd_full = f"python3 byp4xx.py {test_403}  >> {path_full}"
                        cmd = subprocess.Popen(cmd_full,shell=True)
                        cmd.wait()
                        ## Now, we write our command to the output file:
                        file = open(path_full,"a")
                        file.write(f"#####\n##{cmd_full}\n#####\n\n")
                        file.close()
                except:
                    continue
            os.chdir(cur_dir) # go back
    ## NMAP:
    elif cmd == "nmap":
        nmap_path = read_config(cur_dir+"/Config_AutoWeb.ini","PATHS","NMAP")
        cmd_full = f"{nmap_path} -sC -sV -oA -p 80,443 -oA {log_path}nmap_80_443.txt"
        cmd = subprocess.Popen(cmd_full,shell=True)
        cmd.wait()

def banner():
    print("""

     ▄▄▄       █    ██ ▄▄▄█████▓ ▒█████   █     █░▓█████  ▄▄▄▄
    ▒████▄     ██  ▓██▒▓  ██▒ ▓▒▒██▒  ██▒▓█░ █ ░█░▓█   ▀ ▓█████▄
    ▒██  ▀█▄  ▓██  ▒██░▒ ▓██░ ▒░▒██░  ██▒▒█░ █ ░█ ▒███   ▒██▒ ▄██
    ░██▄▄▄▄██ ▓▓█  ░██░░ ▓██▓ ░ ▒██   ██░░█░ █ ░█ ▒▓█  ▄ ▒██░█▀
     ▓█   ▓██▒▒▒█████▓   ▒██▒ ░ ░ ████▓▒░░░██▒██▓ ░▒████▒░▓█  ▀█▓
     ▒▒   ▓▒█░░▒▓▒ ▒ ▒   ▒ ░░   ░ ▒░▒░▒░ ░ ▓░▒ ▒  ░░ ▒░ ░░▒▓███▀▒
      ▒   ▒▒ ░░░▒░ ░ ░     ░      ░ ▒ ▒░   ▒ ░ ░   ░ ░  ░▒░▒   ░
      ░   ▒    ░░░ ░ ░   ░      ░ ░ ░ ▒    ░   ░     ░    ░    ░
          ░  ░   ░                  ░ ░      ░       ░  ░ ░
                                                               ░
        AutoWeb - "Automate The First Day." \n""")

def main():
    if(len(sys.argv))==2:
        cur_dir = os.getcwd() # Where am i?
        web_file = sys.argv[1]
        if not os.path.exists(web_file):
            err(f"Could not open file {web_file} for reading.")
        say_msg(f"Beginning Auto Web with file {web_file}")
        if not os.path.exists("pentest/auto_web"):
            os.makedirs("pentest/auto_web")
            say_msg("pentest/auto_web directory created.")
        with open(web_file) as file:
            for line in file:
                if re.search(r'[a-zA-Z0-9]',line): # no blank lines.
                    url = line.strip()
                    if not re.match(r"^.*/$",url):
                        url = url + "/" # append a forward slash
                    say_msg(f"Scanning URL: {url}")
                    domain = re.sub(r'https?...([A-Za-z0-9-_\.]+)/?.*',r'\1',url)
                    log_dir = f"{os.getcwd()}/pentest/auto_web/{domain}/"
                    if not os.path.exists(log_dir): # check if it exists first
                        say_msg(f"Creating directory pentest/auto_web/{domain}")
                        os.mkdir(log_dir) # make the log directory for this URL/Domain

                    ## Let's log the target URL:
                    url_file = open(log_dir+"target_url.txt","w")
                    url_file.write(url)
                    url_file.close()

                    ## Start the Auto_Web!!:
                    say_msg("Starting SSLScan ... ")
                    run_cmd("sslscan",log_dir,url,cur_dir)
                    say_msg("Starting Nikto ... ")
                    run_cmd("nikto",log_dir,url,cur_dir)
                    say_msg("Starting Wfuzz ... ")
                    run_cmd("wfuzz",log_dir,url,cur_dir)
                    say_msg("Starting Http-shs ... ")
                    run_cmd("http-shs",log_dir,url,cur_dir)
                    say_msg("Starting Http-scan ... ")
                    run_cmd("http-scan",log_dir,url,cur_dir)
                    say_msg("Starting Byp4xx.py ... ")
                    run_cmd("byp4xx",log_dir,url,cur_dir) # TODO get rid of log_dir
                    say_msg("Starting WWWordlist ... ")
                    run_cmd("wwwordlist",log_dir,url,cur_dir) # TODO get rid of log_dir
                    say_msg("Starting pyCORSchk ... ")
                    run_cmd("pyCORSchk",log_dir,url,cur_dir)
                    say_msg("AutoWeb scan completed.")
    else:
        usage("Missing arguments")

if __name__ == "__main__":
    banner()
    main()
