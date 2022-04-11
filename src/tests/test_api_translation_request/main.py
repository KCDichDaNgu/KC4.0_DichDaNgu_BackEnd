import unittest
import requests

class TestTranslationRequest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestTranslationRequest, self).__init__(*args, **kwargs)
        self.base = "http://localhost:8001/{}"
        self.errorpath = "http://localhost:8000/"
        
    def test_translate_request(self):
        url = self.base.format("translation_request")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, "{} is faild".format(url))

    def test_negative_invalid_input(self):
        reponse = requests.get(self.errorpath)
        self.assertNotEqual(reponse, 200, "{} is faild".format(self.errorpath))

    def test_positive(self):
        url = self.base.format("fffffff")
        reponse = requests.get(url)
        self.assertEqual(reponse.status_code, 200, "{} faild".format(url))


    def test_negative_valid_input(self):
        url = self.base.format("translation_request")
        response = requests.get(url)
        response1 = requests.get(url)
        self.assertEqual(response.status_code, 200, "{} is faild".format(url))
        self.assertEqual(response1.status_code, 200, "{} is faild".format(url))

    def test_destructive(self):
        response = requests.get(self.errorpath)
        message = "OK"
        if response.status_code != 200:
            try:
                response.raise_for_status()
            except requests.HTTPError as Exception:
                print(Exception)
                message = Exception
        self.assertEqual(response.status_code, 404, "{} faild".format(self.errorpath))
        self.assertEqual(message, "404 Client Error: Not Found for url: {}".format(self.errorpath), "{} faild".format(self.errorpath))       

if __name__ == "__main__":
    unittest.main(verbosity=2)
