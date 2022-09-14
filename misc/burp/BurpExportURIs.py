#!/usr/bin/env python3
## Burp URI Test
## 1. Right click on target and "Save selected items"
## 2. Run script to extract URIs
import sys ## for args / exit / etc
import os ## read file
import re ## regexp (seems like all my apps use this?)

def usage(msg):
    print(f"Error: {msg}\n")
    print("Usage: python3 BurpExportURIs.py (BURP EXPORT FILE)")
    sys.exit(1)

def main(): ## Are we running as a script?
  if len(sys.argv) != 2: ## Requires a filename as an argument
      usage("No Arguments.")
  else:
      export_file = sys.argv[1] ## grab the file
      if os.path.exists(export_file):
          with open(export_file) as burp_file:
              unique_uris = [] ## Storage for unique URIs
              for line in burp_file:
                  ## FORMAT: <url><![CDATA[https://site.nope/nope?id=nope&nope=nope]]></url>
                  if re.search(r'<url><!.CDATA.http',line): ## We have a URI:
                      uri = re.sub(r'^.*(http[^\]]+).*',r'\1',line).strip()
                      if uri not in unique_uris:
                          unique_uris.append(uri)
              for uri in unique_uris:
                print(uri) ## Done.
      else:
          usage(f"Could not access file {export_file}")

if __name__ == "__main__":
  main()
