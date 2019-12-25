import requests

URL = "http://localhost:8090/session/"
URL1 = "{}1".format(URL)
URL2 = "{}2".format(URL)
URL3 = "{}3".format(URL)

r1 = requests.get(url = URL1) 
r2 = requests.get(url = URL2) 
r3 = requests.get(url = URL3) 

try:
    data = r1.json()
    if data['id'] ==1 and data['bruto'] ==500 and data['truck'] =="524330122":
        print("{} work well".format(URL1))
    else:
        print("{} works bad".format(URL1))

    data = r2.json()
    if data['id'] ==2 and data['bruto'] ==500 and data['truck'] =="524330122" and data['truckTara'] ==200 and data['neto']==300:
        print("{} work well".format(URL2))
    else:
        print("{} works bad".format(URL2))
    
    data = r3.json()
    if data['status'] ==404:
        print("{} work well".format(URL3))
    else:
        print("{} works bad".format(URL3))
except:
    print("{}<id> dont work".format(URL))