import urllib.request
import re

url = "https://t.me/s/trebleexperience"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req)
    html = resp.read().decode('utf-8')
    match = re.search(r'href="([^"]*\?before=\d+)"', html)
    if match:
        print("More link:", match.group(1))
    else:
        print("No more link")
except Exception as e:
    print("Error:", e)
