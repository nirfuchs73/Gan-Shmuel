import requests

URL = "http://localhost:8090/health"

r = requests.get(url = URL) 
try:
    data = r.json()
    if data['status'] ==200:
        print("{} work well".format(URL))
    else:
        print("{} dont work".format(URL))
except:
    print("{} dont work".format(URL))