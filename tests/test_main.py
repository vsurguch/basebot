
import json
import unittest
import requests

url = "http://127.0.0.1:5000/bot/"


class TestMain(unittest.TestCase):

    def test_test(self):
        resp = requests.get(f"{url}test").text
        self.assertEqual(resp, 'ok')

    def test_webhookInfo(self):
        resp = requests.get(f"{url}webhookInfo").json()
        self.assertEqual(resp['ok'], True)

    def test_postUpdate(self):
        body = json.loads('{"update_id": 684932611, "message": {"message_id": 45, "from": {"id": 308634083, "is_bot": false, "first_name": "Vladimir", "username": "YouCube", "language_code": "en"}, "chat": {"id": 308634083, "first_name": "Vladimir", "username": "YouCube", "type": "private"}, "date": 1588077203, "text": "FIND"}}')
        headers = {
            'Content-type': 'application/json'
        }
        resp = requests.post(f"{url}postUpdate", json=body, headers=headers)
        self.assertEqual(resp.text, 'ok')