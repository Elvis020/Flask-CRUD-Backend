import unittest

import requests as requests


class MyTestCase(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000/"

    def test_get_all_articles(self):
        api = requests.get(self.API_URL + "get")
        self.assertEquals(api.status_code, 200)

    def test_get_article(self):
        id_number = 19
        expected_article = {
            "date": "2022-11-20T10:37:22.648157",
            "description": "This is a meme",
            "id": 19,
            "title": "Another addition"
        }
        api = requests.get("{}/{}".format(self.API_URL + "get/", id_number))
        self.assertEquals(api.status_code, 200)
        self.assertDictEqual(api.json(), expected_article)

    def test_get_article_with_incorrect_id(self):
        id_number = 1000
        api = requests.get("{}/{}".format(self.API_URL + "get/", id_number))
        self.assertEquals(api.status_code, 404)

    def test_add_new_article(self):
        new_article = {
            "title": "Testing",
            "description": "This article was added for testing purposes."
        }
        api = requests.post(self.API_URL + "add", json=new_article)
        self.assertEquals(api.status_code, 201)

    def test_update_article(self):
        update_article = {
            "title": "This is the second body edited",
            "description": "Welcome again to the testing world"
        }
        id_number = 20
        api = requests.put("{}/{}".format(self.API_URL + "update/", id_number), json=update_article)
        self.assertEquals(api.status_code, 204)

    def test_delete_article(self):
        id_number = 27  # need to increment this before the whole test suite is executed(see if you can fix this)
        api = requests.delete("{}/{}".format(self.API_URL + "delete/", id_number))
        self.assertEquals(api.status_code, 204)
    