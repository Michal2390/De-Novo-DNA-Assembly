import re
import urllib.request

url = "https://software.broadinstitute.org/software/igv/download"
html = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "ignore")
print("html_len", len(html))

patterns = [
    r"https?://[^\"']+IGV[^\"']+\\.zip",
    r"https?://[^\"']+igv[^\"']+\\.zip",
    r"https?://[^\"']+IGV[^\"']+\\.exe",
    r"https?://[^\"']+igv[^\"']+\\.exe",
    r"https?://[^\"']+IGV[^\"']+\\.jar",
    r"https?://[^\"']+igv[^\"']+\\.jar",
]

links = set()
for pat in patterns:
    links.update(re.findall(pat, html))

for link in sorted(links):
    print(link)

