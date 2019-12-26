import requests
import unittest

URL = "http://localhost:8090/weight"

class testClass(unittest.TestCase):

    def test_weight():
        # direction,truck,containers,weight,unit,produce,force
        r1 = requests.post(url = URL,data={'direction':'out','truck':'7777','containers':'11,22','weight':100,'unit':'gk','produce':'orange','force':'True'})
        data = r1.json()    
        self.assertEqual(data,{"bruto": 200,"id": 10028,"neto": -184,"truck": "7777","truckTara": 100})

if __name__ == '__main__':
    unittest.main()

