# CORSAudit

```
 ▄▄·       ▄▄▄  .▄▄ ·      ▄▄▄· ▄• ▄▌·▄▄▄▄  ▪  ▄▄▄▄▄
▐█ ▌▪▪     ▀▄ █·▐█ ▀.     ▐█ ▀█ █▪██▌██▪ ██ ██ •██  
██ ▄▄ ▄█▀▄ ▐▀▀▄ ▄▀▀▀█▄    ▄█▀▀█ █▌▐█▌▐█· ▐█▌▐█· ▐█.▪
▐███▌▐█▌.▐▌▐█•█▌▐█▄▪▐█    ▐█ ▪▐▌▐█▄█▌██. ██ ▐█▌ ▐█▌·
·▀▀▀  ▀█▄▀▪.▀  ▀ ▀▀▀▀      ▀  ▀  ▀▀▀ ▀▀▀▀▀• ▀▀▀ ▀▀▀
                                     @RackünSec
```
Python implementation to test CORS on a target web server.
## Usage
This tool is quite simple to use. You can now specify whether or not you want to use the Burp Suite proxy (located at 127.0.0.1:8080).
### Basic Usage:
```bash
python3 pyCORSchk.py (URI)
```
### Burp Proxy Usage:
```bash
python3 pyCORSchk.py --burp (URI)
## OR
python3 pyCORSchk.py (URI) --burp
```
