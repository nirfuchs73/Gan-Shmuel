import requests
import unittest

URL = "http://localhost:8090/session/"

class testClass(unittest.TestCase):


    def test_session1(self):
        URL1 = "{}1".format(URL)
        r1 = requests.get(url = URL1)
        data = r1.json()    
        self.assertEqual(data,{'id':1,'bruto':500,'truck':"524330122"})

    def test_session2(self):
        URL2 = "{}2".format(URL)
        r2 = requests.get(url = URL2)
        data = r2.json()    
        self.assertEqual(data,{"bruto": 500,"id": 2,"neto": 300,"truck": "524330122","truckTara": 200})
    
    def test_session3(self):
        URL3 = "{}3".format(URL)
        r3 = requests.get(url = URL3)
        data = r3.json()    
        self.assertEqual(data,{"message": "session non-existent","status": 404})


if __name__ == '__main__':
    unittest.main()

