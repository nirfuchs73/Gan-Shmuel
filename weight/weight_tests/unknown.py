import requests

URL = "http://localhost:8090/unknown"

r = requests.get(url = URL) 
try:
    data = r.json()
    if data['list_id'] ==["22","33"]:
        print("{} work well".format(URL))
    else:
        print("{} works bad".format(URL))
except:
    print("{} dont work".format(URL))
