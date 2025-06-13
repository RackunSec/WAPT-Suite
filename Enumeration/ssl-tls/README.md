# SSLyze-Reporter
A simple Python script to parse the .json output files from [SSLyze](https://github.com/nabla-c0d3/sslyze) This application does not use the SSLyze API. The output from this script should be copy-&-paste friendly for penetration test reports.

## Getting Started
```bash
## Download and install:
git clone https://github.com/RackunSec/WAPT-Suite.git
cd WAPT-Suite/Enumeration/ssl-tls
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 install -r requirements.txt

## Gather SSL information:
python3 -m sslyze (TARGET) --json_out=(TARGET).json

## Run the reporting tool:
python3 sslyze-reporter.py (TARGET).json
```

## TODO
1. LOADS of testing!
