import requests
import unittest

URL = "http://localhost:8090/weight"

class testClass(unittest.TestCase):
# direction,truck,containers,weight,unit,produce,force
    def test_weight(self):
        r1 = requests.post(url = URL,data={'direction':'out','truck':'7777','containers':'11,22','weight':100,'unit':'gk','produce':'orange','force':'True'})
        data = r1.json()    
        self.assertEqual(data,{"bruto": 200,"id": 10028,"neto": -184,"truck": "7777","truckTara": 100})

def test_weight(self):
        r1 = requests.post(url = URL,data={'direction':'out','truck':'7777','containers':'11,22','weight':100,'unit':'gk','produce':'orange','force':'False'})
        data = r1.json()    
        self.assertEqual(data,{"bruto": 200,"id": 10028,"neto": -184,"truck": "7777","truckTara": 100})

if __name__ == '__main__':
    unittest.main()

