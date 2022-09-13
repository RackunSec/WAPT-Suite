# AutoWeb
This tool was designed to automate the first day of a web application penetration test.
```
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
        AutoWeb - "Automate The First Day." 
```
## Setup
Ensure that the Config_AutoWeb.ini file is updated with paths to tools
## Usage
 1. Generate a file with in-scope URLs in it (line by line)
 2. Run the program:
```bash
python3 AutoWeb.py (URLS FILE)
```
 3. This will generate a new directory in the current directory `./pentest/auto_web/(DOMAIN NAME)/`
