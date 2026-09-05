import urllib.request
import re
url = "https://sourceforge.net/projects/andyyan-gsi/files/lineage-21/lineage-21.0-20240217-UNOFFICIAL-arm64_bgS.img.xz/download"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req)
    html = resp.read().decode('utf-8')
    match = re.search(r'refresh".*?url=(.*?)"', html)
    if match:
        print(match.group(1).replace('&amp;', '&'))
    else:
        print("No refresh tag")
except Exception as e:
    print(e)
