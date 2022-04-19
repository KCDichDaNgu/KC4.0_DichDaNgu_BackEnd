import unittest
import requests


class TestLanguageDetectRequest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestLanguageDetectRequest, self).__init__(*args, **kwargs)
        self.baseURL = "http://localhost:8001/{}"

    def test_get_translation_history(self):
        self.response1 = requests.get(self.baseURL.format(
            "translation-history/get-single"))
        self.response2 = requests.get(
            self.baseURL.format("translation-history"))
        # print(self.response1.json())
        self.assertEqual(self.response1.status_code, 200)
        self.assertEqual(self.response2.status_code, 200)

    def test_negative_get_translation_history(self):
        id = "translation-history/get-single?translationHistoryId=aa54200c-c559-4bb4-9952-a1126ce36e13&taskId=86ea0dd7-b52d-4392-a7f9-e32fbacf2c75"
        non_existing_id = id
        self.response = requests.get(self.baseURL.format(non_existing_id))
        body = self.response.json()
        # print(body['data'])
        self.assertEqual(body['data'], [])

    def test_destructive_get_translation_history(self):
        url = "translation-history"
        payload = {}
        self.response = requests.get(self.baseURL.format(url), params=payload)
        # print(self.response.json())
        self.assertNotEqual(self.response.status_code, 200)

    def test_positive_get_translation_history(self):
        url = "translation-history"
        payload = {'page': '1', 'per_page': '5'}
        self.response = requests.get(self.baseURL.format(url), params=payload)
        # print(self.response.json())
        self.assertEqual(self.response.status_code, 200)

    def test_negative_invalid_input_get_translation_history(self):
        url = "translation-history"
        payload = {'pageeeee': '1'}
        self.response = requests.get(self.baseURL.format(url), params=payload)
        # print(self.response.json())
        self.assertEqual(self.response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
