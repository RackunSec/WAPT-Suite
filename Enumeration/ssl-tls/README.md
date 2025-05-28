# ssts-chk
SSL / TLS Checking Tool written in Python3. This tool will perform the following functions:
1. Connect the target given
2. Analyze the secure connection SSL/TLS protocol
3. Analyze the available ciphers for the connection
4. Test each cipher per protocol
5. Reconnect and analyze the certificate itself for items such as:
  * Issuer information
  * Subject Information
  * Hashing / key information
  * Alternative names
  * Version & Serial numbers
  * Key Valid / Expire dates
6. I noticed while developing this tool and testing it that is has a nice side effect in that the Alternative Names in the cert produce more recon/enumeration data than I expected: subdomains and other server domains that the certificate is used! 

## Getting Started
```
git clone https://github.com/RackunSec/WAPT-Suite.git
cd Enumeration/sstls-chk
chmod +x sstls-chk.py
./sstls-chk.py (URL|domain:port)
```

## TODO
1. Add more features
