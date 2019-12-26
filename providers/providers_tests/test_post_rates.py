import requests

file = "/home/eden/Desktop/Providers/Gan-Shmuel/providers/src/in/test1.xlsx"

with open(file, 'rb') as f:
    r = requests.post('http://localhost:8080/rates', files={file: f})

print ("-----> r", r )
if r == "<Response [500]>" or "<Response [200]>":
    print ("very good")
else:
    print ("not so good")