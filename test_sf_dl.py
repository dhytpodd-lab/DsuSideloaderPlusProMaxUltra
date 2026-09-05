import urllib.request
url = "https://downloads.sourceforge.net/project/andyyan-gsi/lineage-21/lineage-21.0-20240217-UNOFFICIAL-arm64_bgS.img.xz"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req)
    print("Code:", resp.getcode())
except Exception as e:
    print("Error:", e)
