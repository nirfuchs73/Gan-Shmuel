import unittest
import requests


class FlaskTestCase(unittest.TestCase):
    def test_health(self):
        print('health_test')
        URL = "http://weight_be_test:8089/health"
        response = requests.get(url=URL,verify=False)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
