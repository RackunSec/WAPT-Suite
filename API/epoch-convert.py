#!/usr/bin/env python3
## 2026 Douglas@RedSiege
## Convert Epoch time to Date
##  Useful for reporting an API key creation date, JWT exp value, etc.
from sys import argv
import time
if len(argv) > 1:
	timestamp = int(argv[1])
	date_str = time.ctime(timestamp)
	print(date_str)
else:
	print("[!] Usage: python3 epoch-convert.py (TIMESTAMP)")
