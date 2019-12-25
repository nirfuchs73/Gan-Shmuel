import unittest
import requests


import sys 
  
def main(out = sys.stderr, verbosity = 2): 
    loader = unittest.TestLoader() 
  
    suite = loader.loadTestsFromModule(sys.modules[__name__]) 
    unittest.TextTestRunner(out, verbosity = verbosity).run(suite) 
    

class FlaskTestCase(unittest.TestCase):
    def test_health(self):
        URL = f"http://localhost:8082/health"

        response = requests.get(url=URL)
        self.assertEqual(response.status_code, 200)


    def test_provider(self):
        URL = f"http://localhost:8082/provider"

        response = requests.post(url=URL, data={'name': 'test_please_remove'})
        self.assertEqual(response.status_code, 200)


    def test_rates_post(self):
        URL = f"http://localhost:8082/rates"

        response = requests.post(url=URL, data={'file': 'test_please_delete'})
        self.assertEqual(response.status_code, 200)


    def test_rates_get(self):
        URL = f"http://localhost:8082/rates"

        response = requests.get(url=URL)
        self.assertEqual(response.status_code, 200)


    def test_truck_put(self):
        URL = f"http://localhost:8082/truck?truck_id=77777&provider_id=2"

        response = requests.put(url=URL, data={'truck_id': '77777', 'provider_id': 2})
        self.assertEqual(response.status_code, 200)


    def test_truck_post(self):
        URL = f"http://localhost:8082/truck"

        response = requests.post(url=URL, data={'id': 'test', 'provider': 0})
        self.assertEqual(response.status_code, 200)

    def test_truck_get(self):
        URL = f"http://localhost:8082/truck"

        response = requests.get(url=URL, data={'from': '200001010000', 'to': '205001010000'})
        self.assertEqual(response.status_code, 200)

    def test_bill_get(self):
        URL = f"http://localhost:8082/bill"

        response = requests.get(url=URL, data={'first_name': 'test'})
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__': 
    with open('testing.out', 'w') as f: 
        main(f) 
        #unittest.main(verbosity=2)
