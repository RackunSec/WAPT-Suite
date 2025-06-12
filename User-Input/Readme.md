# User Input Assessment
The following list of tools were developed as an exercise or to automate tasks when performing user input assessments for web application and or API penetration tests.
## SSRF
[Server-Side Request Forgery](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery) attacks have been much more prevalent for me lately. For more information on SSRF, including the different types ("blind", "half-blind", and "non-blind"), please see [Tenable SSRF plugin](https://www.tenable.com/plugins/was/112439)
### SSRF-Snare
SSRF-Snare is an expansion of the Python3 [HttpServer class](https://docs.python.org/3/library/http.server.html) that responds to incoming SSRF HTTP requests. We can set it to handle specific HTTP methods, what host to listen on, and what port to listen on for incoming requests. The tool will spit out all observed data and parameters and even HTTP headers from the server. It's an easy method for upgrading a [blind SSRF](https://portswigger.net/web-security/ssrf/blind) vulnerability to a [half-blind SSRF](https://www.tenable.com/plugins/was/112439) vulnerability by obtaining additional, possibly sensitive, information from the server.
