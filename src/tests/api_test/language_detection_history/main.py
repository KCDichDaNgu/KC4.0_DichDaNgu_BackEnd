import unittest
import requests

class TestLangDetectionHistoryRequest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestLangDetectionHistoryRequest, self).__init__(*args, **kwargs)
        self.x_url="http://localhost:8001/lang-detection-history/get-single"
        self.x_taskId = "0f684a7e-eb4d-4132-be86-d4652ba7b51a"
        self.x_languageDetectionHistoryId = "7366f96d-73d0-493d-a7eb-bd3563e03f76"
        self.x_wrong_taskId = "sfadsafsdafdsafds"
        self.x_wrong_langDetectionHistoryId = "sfadsafsdafdsafds"

    def test_lang_detection_history_0(self):
        self.response = requests.get(self.x_url)
        self.assertEqual(self.response.status_code, 200)

    def test_lang_detection_history_1(self):
        payload = {
        	"taskId": self.x_taskId,
        }
        self.response = requests.get(self.x_url, params=payload)
        self.assertEqual(self.response.status_code, 200)

    def test_lang_detection_history_2(self):
        payload = {
        	"taskId": self.x_wrong_taskId,
        }
        self.response = requests.get(self.x_url, params=payload)
        self.assertNotEqual(self.response.status_code, 200)
				
    def test_lang_detection_history_3(self):
        payload = {
        	"languageDetectionHistoryId": self.x_languageDetectionHistoryId,
        }
        self.response = requests.get(self.x_url, params=payload)
        self.assertEqual(self.response.status_code, 200)

    def test_lang_detection_history_4(self):
        payload = {
        	"languageDetectionHistoryId": self.x_wrong_langDetectionHistoryId,
        }
        self.response = requests.get(self.x_url, params=payload)
        self.assertNotEqual(self.response.status_code, 200)

    def test_lang_detection_history_5(self):
        payload = {
        	"taskId": self.x_taskId,
        	"languageDetectionHistoryId": self.x_languageDetectionHistoryId,
        }
        self.response = requests.get(self.x_url, params=payload)
        self.assertEqual(self.response.status_code, 200)


if __name__ == '__main__':
		unittest.main(verbosity=2)