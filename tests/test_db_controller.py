import json
import unittest
from datetime import datetime, timedelta

from ..src import db_controller


class TestParseUtils(unittest.TestCase):

    def test_pars_msg(self):
        msg = "01.01.2021 21:20 text"
        try:
            dts, tts, text, important = db_controller.parse_msg(msg)
            self.assertEqual("text", text)
            self.assertEqual(datetime(2021,1,1).timestamp(), dts)
            self.assertEqual(timedelta(hours=21, minutes=20).total_seconds(), tts)

        except ValueError as e:
            self.fail(e)


    def test_pars_msg3(self):
        msg = "21.12.2020"
        try:
            dts, tts, text, important = db_controller.parse_msg(msg)
        except ValueError as e:
            print(e)
            self.assertTrue(True, msg = str(e))


    def test_pars_msg4(self):
        msg = "21.12.2020 21:10"
        try:
            dts, tts, text, important = db_controller.parse_msg(msg)
        except ValueError as e:
            print(e)
            self.assertTrue(True, msg = str(e))


    def test_pars_msg5(self):
        msg = "21.13.2020 21:10"
        try:
            dts, tts, text, important = db_controller.parse_msg(msg)
        except ValueError as e:
            print(e)
            self.assertTrue(True, msg = str(e))


class TestDBController(unittest.TestCase):

    def test_process(self):
        msg = {'chat_id': '308634083', 'text': 'add 01.01.2021 21:20 text!'}
        resp_text = db_controller.DBController.process(msg['chat_id'], msg['text'], fake=True)
        self.assertEqual('ok', resp_text)


if __name__ == '__main__':
    unittest.main()