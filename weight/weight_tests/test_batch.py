import unittest
import requests

class testClass(unittest.TestCase):
    def test_batch(self):
	URL = "http://localhost:8090/batch=weight"
        r = requests.get(url = URL) 
        data = r.json()
        self.assertEqual(data, ["22","33"])


if __name__ == '__main__':
    unittest.main()