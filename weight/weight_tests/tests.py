import unittest
import sys
import requests



class HealthTestCase(unittest.TestCase):
    def test_health(self):
        URL = "http://weight_be_test:8090/health"
        response = requests.get(url=URL)
        self.assertEqual(response.status_code, 200)


class SessionIdTestCase(unittest.TestCase):

    URL = "http://weight_be_test:8090/session1"
    response = requests.get(url=URL)
    @unittest.skipIf(response.status_code != 200, 'cannot get to url')
    def test_session_id1(self):
        URL = "http://weight_be_test:8090/session1"
        response = requests.get(url=URL)
        data = response.json()
        self.assertEqual(data['id'] , 1)
        self.assertEqual(data['bruto'] , 500)
        self.assertEqual(data['truck'] , "524330122")

    URL = "http://weight_be_test:8090/session2"
    response = requests.get(url=URL)
    @unittest.skipIf(response.status_code != 200, 'cannot get to url')
    def test_session_id2(self):
        URL = "http://weight_be_test:8090/session2"
        URL2 = "{}2".format(URL)
        
        r2 = requests.get(url = URL2) 
        data = r2.json()
        self.assertEqual(data['id'] , 2)
        self.assertEqual(data['bruto'] , 500)
        self.assertEqual(data['truck'] , "524330122")
        self.assertEqual(data['truckTara'] , 200)
        self.assertEqual(data['neto'] , 300)


    URL = "http://weight_be_test:8090/session3"
    response = requests.get(url=URL)
    @unittest.skipIf(response.status_code != 200, 'cannot get to url')
    def test_session_id3(self):
        URL = "http://weight_be_test:8090/session"
        URL3 = "{}3".format(URL)

        r3 = requests.get(url = URL3)

        data = r3.json()
        self.assertEqual(data['status'] , 404)


class UnknowTestCase(unittest.TestCase):

    URL = "http://weight_be_test:8090/unknown"
    response = requests.get(url=URL)
    @unittest.skipIf(response.status_code != 200, 'cannot get to url')
    def test_unknow(self):
        URL = "http://weight_be_test:8090/unknown"
        r = requests.get(url = URL) 
        data = r.json()
        self.assertEqual(data['list_id'] , ["22","33"])

def main(out = sys.stderr, verbosity = 2): 
    loader = unittest.TestLoader() 
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(out, verbosity = verbosity).run(suite) 
      
if __name__ == '__main__':
    with open('tests/weight-tests.txt', 'w') as f: 
        main(f)

    with open('tests/weight-tests.txt', 'r') as f: 
        print(f.read())