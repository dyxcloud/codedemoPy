from urllib import request
import sys


url = "https://cdn.v2ex.com/avatar/4bd1/ee3f/275922_large.png123"
req = request.Request(url)
try:
    with request.urlopen(req,timeout=15) as f:
            if f.status == 200:
                data = f.read()
                print(len(data))
            else:
                print(f.status,f.reason)
except :
    print("Unexpected error:", sys.exc_info()[:2])
