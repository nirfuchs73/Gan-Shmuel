import unittest
import requests

class testClass(unittest.TestCase):
    def test_unknown(self):
	URL = "http://localhost:8090/unknown"
        r = requests.get(url = URL) 
        data = r.json()
        self.assertEqual(data, ["33"])


if __name__ == '__main__':
    unittest.main()






