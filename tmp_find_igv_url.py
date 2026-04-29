import re
import urllib.request
from urllib.parse import urljoin

url = "https://software.broadinstitute.org/software/igv/download"
html = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "ignore")
print("html_len", len(html))

hrefs = re.findall(r'href="([^"]+)"', html, re.IGNORECASE)
for href in hrefs:
    low = href.lower()
    if "igv" in low or "download" in low or low.endswith(".zip") or low.endswith(".exe"):
        print(urljoin(url, href))
