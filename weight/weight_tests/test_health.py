import unittest
import requests


class FlaskTestCase(unittest.TestCase):
    def test_health(self):
        print('health_test')
        URL = "http://ec2-54-211-161-133.compute-1.amazonaws.com:8090/health"

        response = requests.get(url=URL)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
