import unittest
import requests

class TestUserGetRequest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUserGetRequest, self).__init__(*args, **kwargs)
        self.x_url="http://localhost:8001/user/"
        self.x_access_token = "b0165e32-ffcf-4683-8488-1e2397a98dca"
        self.x_id = "a885e522-dfb3-4fe0-a819-5b2ea783dc6d"
        self.x_wrong_id = "123456789abcdefksjkjk"
				

    def test_user_get_1(self):
        self.response = requests.get(self.x_url)
        self.assertNotEqual(self.response.status_code, 200)


		# missing authorization header, correct id
    def test_user_get_2(self):
        payload = {
            "id": self.x_id,
        }
        self.response = requests.get(self.x_url, params=payload)
        self.assertEqual(self.response.status_code, 403)


    def test_user_get_3(self):
        headers = {
					"Authorization" : self.x_access_token
				}
        self.response = requests.get(self.x_url, headers=headers)
        self.assertNotEqual(self.response.status_code, 200)

			
    def test_user_get_4(self):
        headers = {
					"Authorization" : self.x_access_token
				}
        payload = {
            "id": self.x_id,
        }
        self.response = requests.get(self.x_url, params=payload, headers=headers)
        self.assertEqual(self.response.status_code, 200)


    def test_user_get_5(self):
        headers = {
					"Authorization" : self.x_access_token
				}
        payload = {
            "id": self.x_wrong_id,
        }
        self.response = requests.get(self.x_url, params=payload, headers=headers)
        self.assertNotEqual(self.response.status_code, 200)


    def test_user_get_6(self):
        headers = {
        	"Authorization" : self.x_access_token
        }
        payload = {
            "id": self.x_id,
        }
        self.response = requests.get(self.x_url, params=payload, headers=headers)
        response_data = self.response.json()

        self.assertEqual(self.response.status_code, 200)
        assert isinstance(response_data["code"], int)
        assert isinstance(response_data["data"], dict)
        assert isinstance(response_data["data"]["id"], str)
        assert isinstance(response_data["data"]["id"], str)
        assert isinstance(response_data["data"]["username"], str)
        assert isinstance(response_data["data"]["firstName"], str)
        assert isinstance(response_data["data"]["lastName"], str)
        assert isinstance(response_data["data"]["avatar"], str)
        assert isinstance(response_data["data"]["email"], str)
        assert isinstance(response_data["data"]["role"], str)
        assert isinstance(response_data["data"]["status"], str)
        assert isinstance(response_data["data"]["totalTranslatedText"], dict)
        assert isinstance(response_data["data"]["totalTranslatedText"]["vi-zh"], int)
        assert isinstance(response_data["data"]["totalTranslatedText"]["vi-en"], int)
        assert isinstance(response_data["data"]["totalTranslatedText"]["vi-km"], int)
        assert isinstance(response_data["data"]["totalTranslatedText"]["vi-lo"], int)
        assert isinstance(response_data["data"]["textTranslationQuota"], dict)
        assert isinstance(response_data["data"]["textTranslationQuota"]["vi-zh"], int)
        assert isinstance(response_data["data"]["textTranslationQuota"]["vi-en"], int)
        assert isinstance(response_data["data"]["textTranslationQuota"]["vi-km"], int)
        assert isinstance(response_data["data"]["textTranslationQuota"]["vi-lo"], int)
        assert isinstance(response_data["data"]["createdAt"], str)
        assert isinstance(response_data["data"]["updatedAt"], str)
        assert isinstance(response_data["message"], str)


if __name__ == '__main__':
		unittest.main(verbosity=2)
