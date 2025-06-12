# SSRF Tools
A collection of tools to work with SSRF vulnerabilities
## SSRF-Snare
SSRF-Snare is a tool that expands upon the Python3 `http.server` method to handling incoming SSRF requests for review. This tool has helped me upgrade blind SSRF to half-blind SSRF during engagements.
### Usage
```

 SSRF-Snare
 2025 @RackunSec
 
 Usage: 
   -P (Local port to listen on)
   -L (Local IP to listen on; "all" also accepted)
   -M (HTTP method GET/POST supported)

 Example:
   python3 ssrf-snare.py -M POST -L 127.0.0.1 -P 8080
 
```
