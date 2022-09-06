# HTTP Secure Header Scanner
Makes a simple HTTP request to a URL and analyzes the headers
## Getting Started
```
git clone https://github.com/RackunSec/http-shs.git
cd http-shs
chmod +x http-shs.py
./http-shs.py
```
## Usage
You can use the `--verbose` argument (optional) to see the actual headers returned. Otherwise they will be analyzed and compared to the findings_db within the findings.json file

## TODO 
I need to analyze the value of the headers for weak/deprecated values and produce a warning to the pentester.
