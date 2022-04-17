import requests
import unittest

header = {
    'Content-Type': 'application/json',
    'Accept-Encoding':  'gzip, deflate, br',
    'Connection': 'keep-alive'
}


def url_gen(path):
    form = "http://localhost:8001/{}".format(path)
    return form


def detect_lang(URL, payload):
    response = requests.post(URL, json=payload, headers=header)
    if response.status_code != 200:
        try:
            response.raise_for_status()
        except requests.HTTPError as exception:
            return None, response.status_code, exception
    data = response.json()
    return data['data']['taskName'], response.status_code


def translate(URL, payload):
    response = requests.post(URL, json=payload, headers=header)
    if response.status_code != 200:
        try:
            response.raise_for_status()
        except requests.HTTPError as exception:
            return None, response.status_code, exception
    data = response.json()
    return data['data']['taskName'], response.status_code


class test_detect_lang(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(test_detect_lang, self).__init__(*args, **kwargs)

        self.path = "detect-lang"
        self.baseURL = "http://localhost:8001/detect-lang"


    def test_status_code(self):
        task_name, status_code = detect_lang(
            url_gen(self.path), {'sourceText': 'Hello'})
        self.assertEqual(status_code, 200, 'Status code of endpoint detect-lang failed')

    def test_task_name(self):
        task_name, status_code = detect_lang(
            url_gen(self.path), {'sourceText': 'Hello'})
        self.assertEqual(
            task_name, 'public_plain_text_language_detection', 'Detect task name of endpoint detect-lang failed')


class test_translate(unittest.TestCase):    
    def __init__(self, *args, **kwargs):
        super(test_translate, self).__init__(*args, **kwargs)

        self.path = 'translate'
        self.baseURL = "http://localhost:8001/translate"

    def test_status_code(self):
        task_name, status_code = translate(url_gen(
            self.path), {"sourceText": "Hello", "targetLang": "vi", "sourceLang": "en"})
        self.assertEqual(status_code, 200, 'Status code of endpoint translate failed')

    def test_task_name(self):
        task_name, status_code = translate(url_gen(
            self.path), {"sourceText": "Hello", "targetLang": "vi", "sourceLang": "en"})
        self.assertEqual(task_name, 'public_plain_text_translation',
                         'Detect task name of endpoint tranlate faied')


if __name__ == "__main__":
    unittest.main(verbosity=2)
