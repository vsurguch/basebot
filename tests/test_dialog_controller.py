
import unittest

from ..src.dialog_controller import DialogController
from ..src.parse_utils import convertDateStr, convertTimeStr, convertPhoneStr
from ..src.dbmanage import dbmain_termin


class TestDialogController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.controller = DialogController()

    def setUp(self):
        dbmain_termin(create=True, verbose=False)

    def tearDown(self):
        pass


    # def test_process(self):
    #     msg = {'chat_id': '308634083', 'text': 'hello'}
    #     result = self.controller.process(msg['chat_id'], msg['text'], cmd='')
    #     self.assertEqual("ok", result)


    def test_getNextNone(self):
        msg = {'chat_id': '308634083', 'text': 'John'}
        row = self.controller.RowClass(chat_id=int(msg['chat_id']), complete=False)
        next0, next1 = self.controller.getNextNone(row)
        self.assertEqual('name', next0)
        self.assertEqual('date', next1)


    def test_convertRowToStr(self):
        msg = {'chat_id': '308634083', 'text': 'John'}
        row = self.controller.RowClass(chat_id=int(msg['chat_id']),
                                       name="John",
                                       date=convertDateStr("12.12.2020"),
                                       time=convertTimeStr("20:20"),
                                       phone=79263231575,
                                       text="Text",
                                       complete=False)
        result = self.controller.convertRowToStrList(row)
        expected = ["chat_id: 308634083", "name: John", "date: 12-12-2020", "time: 20:20", "phone: +7(926)323-15-75", "text: Text", "complete: False"]
        self.assertEqual(expected, result)


    def test_getLastNotNone(self):
        msg = {'chat_id': '308634083', 'text': 'John'}
        row = self.controller.RowClass(chat_id=int(msg['chat_id']),
                                       name="John",
                                       phone=None,
                                       date=None,
                                       time=None,
                                       complete=False)
        last = self.controller.getLastNotNone(row)
        self.assertEqual('name', last)


    def test_revert(self):
        msg = {'chat_id': '308634083', 'text': 'John'}
        row = self.controller.RowClass(chat_id=int(msg['chat_id']),
                                       name="John",
                                       phone=None,
                                       date=None,
                                       time=None,
                                       complete=False)
        self.controller.connection.put(row)
        rows = self.controller.connection.get(self.controller.RowClass)
        self.assertEqual(1, len(rows))
        last = self.controller.getLastNotNone(rows[-1])
        self.assertEqual('name', last)
        self.controller.revert(rows[-1], last)
        rows = self.controller.connection.get(self.controller.RowClass)
        self.assertEqual(1, len(rows))
        self.assertEqual(None, rows[-1].name)

