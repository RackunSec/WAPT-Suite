# WAPT Suite
This is a collection of tools that I use during web application penetration tests. A lot of these exist elsewhere and I mainly made this repository as an exercise and I use it in most of my engagements. 
## What's Included
Below is a summary of some of the included tools and documentation
### Enumeration
 * [HTTP-SHC](Enumeration/http-headers/) - HTTP security headers checks
 * [Web-Comment-Scrape](Enumeration/comments/) - Scrapes a page for HTML and JS comments
 * [HTTP-Scan](Enumeration/http-scan/) - Makes HTTP requests from targets file and logs responses
 * [Site-Map-Enum](Enumeration/site-maps/) - Enumeration of site maps identified during web application tests
 * [SSL-TLS](Enumeration/ssl-tls/) - This was just an exercise with Python for me - use SSLScan for this type of testing
 * [TimedUserEnum](Enumeration/username/) - A WIP, PoC for analyzing timed server responses for valid/invalid usernames of web apps

### User-Input Testing
 * [SSRF-Lure](User-Input/ssrf-lure/) - An HTTP server to handle incoming SSRF requests
 
### Vuln Scanning 
 * [AutoWeb](Automation/) - Automate the first day of web application penetration test
 * [CORSAudit](Enumeration/cors/) - This tool checks for CORS-related security issues

### Miscellaneous
 * [UA-Util](Miscellaneous/ua-util.py) - HTTP header User-Agent Utility (randomizing for evasion, etc)
 * [Dredgeon](Miscellaneous/entropy) - Dredges through a file looking for potential web-related sensitive information.
 * [BurpExportURIs](Miscellaneous/burp) - Extract URIs from Burp Suite's project files.

### Wordlists
This is a set of wordlists that I have generated over the years of web application penetration testing.
 * [Wordlists](Miscellaneous/wordlists/) - Collection of all wordlists
 * [WWWordlist](Miscellaneous/wordlists/tools/wwwordlist.py) - This tool scrapes a page and generates a word list
