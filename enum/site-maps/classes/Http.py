# Python module for HTTP requests and handling of XML
# 2022 Douglas Berdeaux
import requests  # make http requests
from classes.Style import Style
from bs4 import BeautifulSoup  # for parsing the XML
import re
import os  # for directory creation/path stuff


class Http:
    # Initialization:
    def __init__(self):
        self.style = Style()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"
        }
        self.interesting = [
            "backup",
            "bak",
            "api",
            "token",
            "secret",
            "credentials",
            "mfa",
            "config",
            "passw",
            "usern",
            "azure",
            "ldap",
            "robots",
            "temp",
            "old",
            "sensitive",
            "priv",
            "dev",
            "test",
            "staging",
            "staged",
            "donot",
            "server-status",
            "archive",
            "archiva",
            "filesystem",
            "files",
            "camera",
            "security",
            "footage",
            "adfs",
            "topsec",
            "sql",
            "database",
            "mariadb",
            "postgre",
            "sqlite",
            "prod",
            "multifactor",
            "authoriz",
            "roles",
            "smb",
            "share",
            "activedir",
            "aws",
            "s3",
            "about.php",
            "internal",
            "intranet",
            "crypto",
            "stash",
            "logs",
            "cache",
            "session",
            "account",
            "shell",
            "pwn",
            "access",
        ]

    # This returns an object that can be used for BeautifulSoup:
    def getxml(self, url):
        try:
            reqdata = requests.get(url, headers=self.headers)  # get the URL
            # create the log directory:
            domain = re.sub("https?:..([^/]+).*", r"\1", url)
            file = domain + "/" + domain + "-sitemap.xml-urls.txt"
            if not os.path.isdir(domain):
                os.mkdir(domain)
            with open(file, "w") as fh:  # open the file handler for logging
                soup = BeautifulSoup(
                    reqdata.text, features="lxml"
                )  # send text of HTTP response into BS
                tags = soup.find_all("loc")  # Pull out the "loc" tags only
                sitemaps = []  # store nested sitemaps
                sites = []  # to return for further inspection
                for site in tags:  # loop over the "loc" tags and print the text only:
                    sites.append(site.text)
                    fh.write(site.text + "\n")  # Write the site to the file.
                    self.check4interesting(site.text)  # check 4 interesting words
                    # List nested sitemaps:
                    if re.search("sitemap.*\.xml", site.text):
                        url2 = re.sub(
                            "(sitemap.*\.xml)",
                            rf"{self.style.RED}\1{self.style.CMNT}",
                            site.text,
                        )
                        print(
                            f"{self.style.arrow()} Nested Sitemap: {url2}{self.style.RST}"
                        )
                        sitemaps.append(site.text)
                print(f'{self.style.FILE}{self.style.CMNT}Log file written: {self.style.RED}"{file}" {self.style.parens(str(len(sites))+" URLs discovered")}{self.style.RST}')
            # Crawl all nested sitemaps:
            if len(sitemaps) > 0:
                if (
                    len(sitemaps) == 1
                ):  # This is to check if only 1 sitemap and it's itself.
                    if sitemaps[0] == url:
                        pass
                else:
                    ans = input(
                        f"{self.style.ques()} Would you like me to crawl nested sitemaps? {self.style.LMGE}({self.style.RED}{len(sitemaps)}{self.style.LMGE}) [{self.style.RED}y/n{self.style.LMGE}]? {self.style.RST}"
                    )
                    if ans == "y":
                        if not os.path.isdir(domain + "/nested-sitemaps"):
                            os.mkdir(
                                domain + "/nested-sitemaps"
                            )  # make the sub directory.
                        for sitemap in sitemaps:
                            if sitemap == url:
                                pass
                            self.style.ok(
                                f"Crawling: {self.style.RED}{sitemap}{self.style.RST}"
                            )
                            try:
                                req = requests.get(sitemap, headers=self.headers)
                                file = re.sub(
                                    "[^0-9a-zA-Z_.-]", "-", sitemap
                                )  # create a filename to store it.
                                file = (
                                    domain
                                    + "/nested-sitemaps/"
                                    + re.sub("^.*(sitemap.*\.xml)", r"\1", file)
                                )
                                with open(
                                    file, "w"
                                ) as fh:  # open the file handler for logging
                                    self.getxml(
                                        sitemap
                                    )  # get the text of the nested sitemap
                                    soup = BeautifulSoup(
                                        req.text, features="lxml"
                                    )  # parse the XML
                                    tags = soup.find_all("loc")
                                    for site in tags:
                                        self.check4interesting(site.text)
                                        fh.write(site.text + "\n")
                                self.style.ok(f"{self.style.FILE}  Log file written as {file}")
                            except Exception as e:
                                self.style.fail(f"Fetching URL {sitemap} failed: {e}")
            return sites  # This returns the list for the "--scrape" functionality.
        except Exception as e:
            self.style.fail(f"Fetching URL {url} failed: {e}")

    # Scraping actual source code of each page:
    def getCode(self, url):
        domain = re.sub("https?:..([^/]+).*", r"\1", url)  # grab JUST the domain name
        file = re.sub("^https?:..[^/]+/", "", url)  # remove the protocol prefix
        file = re.sub("/", "-", file)  # chnage all forwardslashes to dashes.
        file = domain + "/" + re.sub("/", "-", file) + ".txt"
        try:
            req = requests.get(url, headers=self.headers)
            with open(file, "a") as fh:  # with is Pythonic.
                fh.write(req.text + "\n")
            return
        except Exception as e:
            self.style.fail(f"Fetching URL {url} failed: {e}")

    # Check the URLs for interetsing terms:
    def check4interesting(self, url):
        for inter in self.interesting:
            if re.search(f"[/\._-]{inter}", url, re.IGNORECASE):
                url = re.sub(inter, self.style.RED + inter + self.style.LMGE, url)
                print(
                    f"{self.style.info()}{self.style.CMNT} Interesting:{self.style.LMGE} {url}{self.style.RST}"
                )
