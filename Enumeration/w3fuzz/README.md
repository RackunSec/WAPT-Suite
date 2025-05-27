# w3fuzz
W3fuzz is a lightweight, single file, multiprocessor, web application and web server fuzzer. No third-party dependencies required. This project is targeted towards web application penetration testers and web bug bounty hunters. The output of W3fuzz is report friendly and fits within a standard-sized terminal. No colors are used to ensure that light-themed terminals have enough contrast for professional penetration test/bug bounty reports. 

This project is a work in progress. 

## Usage
```
              __       ___                           
            /'__`\   /'___\                          
 __  __  __/\_\L\ \ /\ \__/  __  __  ____    ____    
/\ \/\ \/\ \/_/_\_<_\ \ ,__\/\ \/\ \/\_ ,`\ /\_ ,`\  
\ \ \_/ \_/ \/\ \L\ \ \ \_/\ \ \_\ \/_/  /_\/_/  /_ 
 \ \___x___/'\ \____/ \ \_\  \ \____/ /\____\ /\____\
  \/__//__/   \/___/   \/_/   \/___/  \/____/ \/____/             
 
 Web Application Enumeration via Fuzzing
 2025, @RackünSec
          
 Usage: 
    -u (TARGET URL)
    -H (HTTP Headers: e.g.: "User-Agent:Mozilla Browser;Authorization:Bearer ...")
    -d (HTTP POST data: e.g.: "id=13&user=administrator&session=true")
    -c (HTTP Cookies, delimited with semicolons)
          
 Filtering:
    -[s/h]c (int): Show/Hide responses that match HTTP code
    -[s/h]l (int): Show/Hide http responses that match HTTP code
    -[s/h]r (regexp): Show/Hide http responses that match Regexp in body
    -[s/h]s (String): Show/Hide http responses that match a string in body
```
### "FUZZ"
Much like [wfuzz](https://github.com/xmendez/wfuzz), w3fuzz takes a `FUZZ` keyword that can be in either HTTP request headers, HTTP POST and GET parameters, or in URLs. Simple put the FUZZ keyword into one of the `-d`, `-u`, or `-H` arguments to have w3fuzz use it as an insertion point. Only one insertion point is allowed. An example is shown below.
```bash
python3 w3fuzz.py -u https://FUZZ/robots.txt -w wordlist.txt -hc 404
```

### Filtering Responses
My favorite aspect of Wfuzz was the ability to fine-tune your filters. W3fuzz has multiple ways of filtering HTTP responses to help you identify exactly what you are looking for. The following section demonstrates examples of different filter types that are compatible with w3fuzz.

#### Regular Expressions
To filter HTTP responses where the body contains (or not) specific string patterns, you can use regular expressions like so:
```bash
python3 w3fuzz.py -u https://acme.corp/FUZZ.aspx -sr '[Pp][Aa][Ss]{2}[Ww][oO][Rr][Dd]' -hc 404 -w wordlist.txt
```
The above command will filter out all HTTP responses that do not contain the word password (any case).
```bash
python3 w3fuzz.py -u https://acme.corp/FUZZ.aspx -hr '[Pp][Aa][Ss]{2}[Ww][oO][Rr][Dd]' -hc 404 -w wordlist.txt
```
The above command will filter out all HTTP responses where the body DOES contain the word password (any case).

#### Response Code
Filtering on response code using Wfuzz over the years was a huge crutch for quickly identifying target pages and content. To filter on HTTP response code, review the following command, specifically the `-hc` argument.
```bash
python3 w3fuzz.py -u https://acme.corp/FUZZ.aspx -hc 404 -w wordlist.txt
```
The above command will NOT show HTTP responses with the status code of `404`
```bash
python3 w3fuzz.py -u https://acme.corp/FUZZ.aspx -sc 404 -w wordlist.txt
```
The above command will show all HTTP responses with the status code of `404`

#### Strings
Filtering on HTTP responses whose body contains a specific string is possible using w3fuzz. An example is shown below.
```bash
python3 w3fuzz.py -u http://acme.corp/FUZZ.php -w wordlist.txt -ss "password" -hc 404
```
The above command will only show (`-ss`) HTTP responses whose body contains the case-sensitive string of "password".
## Output Example
The listing below shows what the output of W3fuzz looks like:
```
python3 w3fuzz.py -w wordlist.txt -u http://acme.corp/FUZZ -hc 404
 Scan Configuration:
 -------------------------
 Target URL: http://acme.corp/FUZZ
 Request Type: GET
 Filter Applied: Hide Status Code of 404
 Insertion Point Location: URL
 Wordlist: wordlist.txt

 Scan Began: 2025-03-12 12:34:24.376660 

 Payload            Status              Length              
 ------------------------------------------------
 robots.txt         200                 0                   
 .htaccess          403                 274                 
 server-status      403                 27266               

 Total Requests Made in this Session: 42 
```
The Scan Configuration segement shows you and your clients your goal during the enumeration session. The tabular output shows the results and may not be pretty depending on your wordlist file contents. Longer lines may produce line breaks in the terminal output. Finally, the footer is simply to show off some statistics about the enumeration session. 

## TLS
W3fuzz will not complain about TLS issues (at least it shouldn't). If you are testing TLS issues specifically, I recommend using another tool, such as [SSLyze](https://github.com/nabla-c0d3/sslyze).

## To Do
 * Tasks to do ...
 * Still under development ... 