# Py-Web-Tools Suite
This is a collection of tools that I use during penetration tests. A lot of these exist elsewhere and I mainly made this repository as an exercise. 
## Tools
A full list of tools
### Enumeration
 * [http-shs](enum/http-headers/) - HTTP security headers checks
 * [web-comment-scrape](enum/comments/) - Scrapes a page for HTML and JS comments
 * [http-scan](enum/http-scan/) - Makes HTTP requests from targets file and logs responses
 * [site-map-enum](enum/site-maps/) - Enumeration of site maps identified during web application tests
 * [ssl-tls](enum/ssl-tls/) - This was just an exercise with Python for me - use SSLScan for this type of testing
 * [TimedUserEnum](enum/username/) - A WIP, PoC for analyzing timed server responses for valid/invalid usernames of web apps
 
### Vuln Scanning 
 * [AutoWeb](auto/) - Automate the first day of web application penetration test
 * [pyCORSchk](enum/cors/) - CHeck for CORS-related security issues

### Miscellaneous
 * [wwwordlist](misc/wordlists/) - This tool scrapes a page and generates a word list
 * [UA-util](misc/ua-util.py) - HTTP header User-Agent Utility (randomizing for evasion, etc)
