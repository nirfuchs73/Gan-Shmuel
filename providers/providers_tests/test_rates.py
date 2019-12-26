import unittest
import json, requests

API_ENDPOINT = "http://127.0.0.1:8080"

data = {'file':'test1.xlsx'}
r = requests.post(API_ENDPOINT, data=json.dumps(data))
print (r)


        