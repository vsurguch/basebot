
import unittest


from ..src.main_controller import access_denied, processUpdate

url = "http://127.0.0.1:5000/bot/"


class TestUtils(unittest.TestCase):

    def test_access_denied(self):
        resp = access_denied('308634083')
        self.assertTrue(resp.json()['ok'])

    def test_processUpdate(self):
        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False, "first_name": "Vladimir", "username": "YouCube", "language_code": "en"}, "chat": {"id": 308634083, "first_name": "Vladimir", "username": "YouCube", "type": "private"}, "date": 1588075894, "text": "\u041f\u0440\u0438\u0432\u0435\u0442"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual(resp_text, 'ok')
