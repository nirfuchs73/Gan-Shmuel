import unittest
import requests


class FlaskTestCase(unittest.TestCase):
    def test_health(self):
        URL = "http://localhost:8090/health"
        response = requests.get(url = URL)
        data = response.json()   
        self.assertEqual(data, {"message": "OK","status": 200})

if __name__ == "__main__":
    unittest.main()
