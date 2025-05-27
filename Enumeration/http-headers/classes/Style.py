#!/usr/bin/env python3
## 2022 Douglas Berdeaux (@RackunSec)
## HTTP Secure Header Scanner:
##   Analyzes HTTP response headers for missing security header values
##
## Style class
##
from sty import fg,bg
import re # for variable message colors
class Style:
    def __init__(self,darkmode):
        self.darkmode = darkmode
        if  not self.darkmode:
            self.BLK='\033[1m'+fg(233) # Black Text -> use with "BG" values below
            self.RED=fg(197) # pretty red
            self.YLL=fg(226) # pretty yellow
            self.GRN=fg(46) # nice green color
            self.RST='\033[0m' # reset the color to terminal default
            self.LMGE='\033[95m' # light magenta
            self.CMNT='\033[37m\033[3m' # comment-like text
            self.PPIN=fg(171) # purplish-pink
            self.PPUR=fg(135) # nice purple
            self.PINK=fg(201) # pink color
            self.NET=self.PPUR+' 🖧  '+self.RST # show network icon
            self.FILE=self.PPUR+' 🗁  '+self.RST # Show file icon
            self.OK = f"\033[3m{fg(200)}" # OK text color only
            self.BLUE=fg(39)
            self.ORAN=fg(208)
            self.BLUEBG=bg(39)
            self.ORANBG=bg(208)
            self.REDBG=bg(197)
            self.YLLBG=bg(226)
        else:
            self.BLK='\033[0m' # Black Text -> use with "BG" values below
            self.RED='\033[0m' # pretty red
            self.YLL='\033[0m' # pretty yellow
            self.GRN='\033[0m' # nice green color
            self.RST='\033[0m' # reset the color to terminal default
            self.LMGE='\033[0m' # light magenta
            self.CMNT='\033[0m' # comment-like text
            self.PPIN='\033[0m' # purplish-pink
            self.PPUR='\033[0m' # nice purple
            self.PINK='\033[0m' # pink color
            self.NET='\033[0m' # show network icon
            self.FILE='\033[0m' # Show file icon
            self.OK = '\033[0m' # OK text color only
            self.BLUE='\033[0m'
            self.ORAN='\033[0m'
            self.BLUEBG='\033[0m'
            self.ORANBG='\033[0m'
            self.REDBG='\033[0m'
            self.YLLBG='\033[0m'

    ## Warning Messge:
    def warn(self):
        return f"\033[3m{self.YLL}⚠ Warning: "

    ## Print an arrow for indentation:
    def arrow(self): # This is just " --> " but fancyier.
        return f"{self.RED} →{self.RST}"

    ## Prompt User for Question:
    def ques(self): # This just asks "[?]" much fancier:
        return f"{self.PINK}[{self.PPUR}?{self.PINK}]{self.RST}"

    ## Print Information to user:
    def info(self): # This just says "[i]" much fancier:
        return f"{self.PINK}[{self.PPUR}i{self.PINK}]{self.RST}"

    ## Print [ OK ]:
    def ok(self,msg): # This just says "[ok]" much fancier:
        print(f"\033[3m{fg(200)} ✔ {fg(201)}{msg}{self.RST}")

    ## Custom Brackets:
    def brackets(self,msg): # Custom, colored square brackets [ msg ]
        return f"{self.PINK}[{self.PPUR}{msg}{self.PINK}]{self.RST}"

    ## Custom Parenthesis:
    def parens(self,msg):
        return f"{self.PINK}({self.PPUR}{msg}{self.PINK}){self.RST}"

    ## Print Failures:
    def fail(self,msg): # This handles all failures during runtime
        msg = re.sub("([\[\]])",f"{self.LMGE}\\1{self.RED}",msg) # color the brackets
        msg = re.sub("([\(\)])",f"{self.LMGE}\\1{self.RED}",msg) # color the brackets
        print(f"\033[3m{fg(196)} ✖ {self.RED}{msg}{self.RST}")

    ## Print headings:
    def header(self,msg): # 28 total
        header_len = len(msg)
        divider = f"\n {self.RED}+"
        for i in range(13):
            divider += f"{self.PPIN}-{self.PPUR}-"
        divider += f"{self.RED}+{self.RST}\n"
        print(divider+f" {self.PINK}▒ {msg} {' ' * (23-header_len)} ▒{self.RST}"+divider)

    def usage(self,title):
        print(f"""{self.RED}
 __     __   __                       __
|  |--.|  |_|  |_.-----.  ___  .-----.|  |--.-----.
|     ||   _|   _|  _  | |___| |__ --||     |__ --|
|__|__||____|____|   __|       |_____||__|__|_____|
                 |__|
    {self.LMGE}{title}{self.RST}
        """)
        ## Update the following for your specific app's usage:
        self.header("HELP CMD")
        usage = "Usage: ./http-shs.py (url) (--verbose)"
        ## This will color it for you:
        usage = re.sub("([\[\]])",f"{self.LMGE}\\1{self.CMNT}",usage) # color the brackets
        usage = re.sub("([\(\)])",f"{self.LMGE}\\1{self.CMNT}",usage) # color the brackets
        usage = re.sub("(./[^\s]+)",f"{self.GRN}\\1{self.RST}",usage) # color the brackets
        usage = f"{self.CMNT} "+usage
        print(f"{self.ques()}{usage}{self.RST}\n")
