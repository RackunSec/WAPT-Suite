# Sitemap Enum
Crawl and scrape a website's sitemap.xml file during enumeration phase of a penetration test.
## Download and Requirements
To download the repository use the following command:
```
git clone https://github.com/RackunSec/sitemap-enum.git
```
This script does require some Python libraries. You can install them with the following command:
```
python3 -m pip install -r requirements.txt
```
## Usage
### General
To get (and log) the sitemap contents, use the following syntax:
```
./sitemap-enum.py (sitemap url)
```
You will be asked to scrape nested sitemaps (if discovered).
#### Scraping
To scrape each individual sitemap url you can either add the `scrape` command,
```
./sitemap-enum.py (sitemap url) --scrape
```
or import the `Http.py` module and pass your URL(s) into the `getxml()` method
