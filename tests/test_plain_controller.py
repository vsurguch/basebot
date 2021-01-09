import json
import unittest


from ..src.plain_controller import PlainController
from ..src.weather_controller import WeatherContoller


# from io import BytesIO
#
# response = requests.get('https://arxiv.org/pdf/1506.01497.pdf')
# print('response recieved')
#
# # data = BytesIO(response.content)
# with open('file.pdf', 'wb') as f:
#     f.write(response.content)
# with open('last_id', 'r') as f:
#     id = int(f.read())
#     print(id)


class TestPlainController(unittest.TestCase):

    def test_process(self):
        msg = {'chat_id' : '308634083', 'text': 'test'}
        resp_text = PlainController.process(msg['chat_id'], msg['text'], fake=True)
        self.assertEqual('test', resp_text)

    def test_processThreading(self):
        msg = {'chat_id': '308634083', 'text': 'test'}
        resp_text = PlainController.processThreading(msg['chat_id'], msg['text'])
        self.assertEqual(resp_text, "Processing started in separate thread")


class TestWeatherController(unittest.TestCase):

    def test_process(self):
        msg = {'chat_id': '308634083', 'text': 'Riga'}
        resp_text = WeatherContoller.process(msg['chat_id'], msg['text'], fake=True)
        self.assertTrue(resp_text.startswith("Weather for Riga"))

    def test_processThreading(self):
        msg = {'chat_id': '308634083', 'text': 'Paris FR'}
        resp_text = WeatherContoller.processThreading(msg['chat_id'], msg['text'])
        self.assertEqual(resp_text, "Processing started in separate thread")
