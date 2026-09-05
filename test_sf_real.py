import urllib.request
url = "https://downloads.sourceforge.net/project/keepass/KeePass%202.x/2.54/KeePass-2.54.zip"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req)
    print("Code:", resp.getcode())
    print("URL:", resp.geturl())
except Exception as e:
    print("Error:", e)
