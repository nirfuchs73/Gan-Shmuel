import requests
import unittest

# /item/<id>?from=t1&to=t2

class testClass(unittest.TestCase):

    def test_item(self):
    	URL = "http://localhost:8090/item/2"
        r1 = requests.get(url = URL)
        data = r1.json()    
        self.assertEqual(data,{"id": "2","session": [],"tara": None})

    def test_item(self):
    	URL = "http://localhost:8090/item/2"
        r1 = requests.get(url = URL)
        data = r1.json()    
        self.assertEqual(data,{"id": "2","session": [],"tara": None})

    def test_item(self):
    	URL = "http://localhost:8090/item/34"
        r1 = requests.get(url = URL)
        data = r1.status_code    
        self.assertEqual(data,400)

    def test_item(self):
    	URL = "http://localhost:8090/item/33"
        r1 = requests.get(url = URL)
        data = r1.json()    
        self.assertEqual(data,{"id": "33","session": [10011,10010,10012,10013,10014,10015,10016,10017,10018,10019,10020,10021],"tara": None})

    def test_item(self):
    	URL = "http://localhost:8090/item/33"
        r1 = requests.get(url = URL)
        data = r1.json()    
        self.assertEqual(data,{"id": "33","session": [10011,10010,10012,10013,10014,10015,10016,10017,10018,10019,10020,10021],"tara": None})        

	def test_item(self):
		URL = "http://localhost:8090/item/7777"
		r1 = requests.get(url = URL)
		data = r1.json()    
		self.assertEqual(data,{"id": "7777","session": [10027,10028],"tara": 100})        


if __name__ == '__main__':
    unittest.main()

