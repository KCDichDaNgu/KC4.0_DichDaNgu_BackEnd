import requests
import unittest


def url_gen(path):
    form = "http://localhost:8001/{}".format(path)
    return form


def detect_lang(URL, payload):
    response = requests.post(URL, data=payload)
    if response.status_code != 200:
        try:
            response.raise_for_status()
        except requests.HTTPError as exception:
            return None, response.status_code, exception

    

    return response.text, response.status_code, 'OK'


class test_detect_lang(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(test_detect_lang, self).__init__(*args, **kwargs)

        self.path = "detect-lang"
        self.baseURL = "http://localhost:8001/detect-lang"

        

    def test_ok_case(self):
        lang_detected, status_code, message = detect_lang(url_gen(self.path), {'sourceText': 'Hello World'})
        self.assertEqual(status_code, 200, 'Status code failed')
        self.assertEqual(lang_detected, 'en', 'Detect language failed')

    def test_not_ok_test(self):
        print("Fail")


if __name__ == "__main__":
    unittest.main(verbosity=2)
