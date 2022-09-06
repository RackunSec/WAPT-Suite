# web-comment-scrape
A web comment scrape tool to quickly pull out only comments from the DOM of a target URI. This tool searches (using regexp) for the following items in the HTTP response body:
* Single line JS comments using `//`
* Single line JS comments using `/* */`
* Single line HTML comments using `<!-- .* -->`
* Multi line HTML comments using `<!-- \n -->`
## Getting Started
```
git clone https://github.com/RackunSec/web-comment-scrape.git
cd web-comment-scrape
chmod +x wcs.py
./wcs.py
```
## Usage
Simply pass a URI to the applciation:
```
./wcs.py (url)
```
## TODO
Find new syntaxes of comments to discover
