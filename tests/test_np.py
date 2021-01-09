
import unittest
from datetime import datetime


from ..src.dbmanage import dbmain_nextplease as dbmain
from ..src.dbutils import getRow
from ..src.main_controller_np import processUpdate
from ..src.np_controller import NextPleaseController, SelectDate

url = "http://127.0.0.1:5000/bot/"


class TestUtils(unittest.TestCase):


    conn = NextPleaseController.connection
    RowClass = getRow("appointments", ['chat_id', 'name', 'phone', 'date', 'time', 'complete'])


    def setUp(self):

        dbmain(create=True, verbose=False)


    def test_processUpdateNormalFlow(self):

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "записаться"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("Сообщите фамилию пациента", resp_text)
        rows = self.conn.get(NextPleaseController.RowClass)
        self.assertEqual(1, len(rows))
        self.assertEqual(308634083, rows[0].chat_id)

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "Сургуч"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("Укажите контактный телефон", resp_text)
        rows = self.conn.get(NextPleaseController.RowClass)
        self.assertEqual(1, len(rows))
        print(rows[0])
        self.assertEqual('Сургуч', rows[0].name)

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "+792632231575"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("Выберете дату", resp_text)
        rows = self.conn.get(NextPleaseController.RowClass)
        self.assertEqual(1, len(rows))
        print(rows[0])
        self.assertEqual(792632231575, rows[0].phone)

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "12-01-2021"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("и время", resp_text)
        rows = self.conn.get(NextPleaseController.RowClass)
        self.assertEqual(1, len(rows))
        print(rows[0])
        self.assertEqual(datetime(2021, 1, 12).timestamp(), rows[0].date)

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "13:30"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("ok", resp_text)
        rows = self.conn.get(NextPleaseController.RowClass)
        self.assertEqual(1, len(rows))
        print(rows[0])
        self.assertEqual(13 * 60 * 60 + 30 * 60, rows[0].time)
        self.assertEqual(True, rows[0].complete)


    def test_processUpdateNotStarted(self):

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "Иванов"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("Сначала необходимо начать новую запись", resp_text)
        rows = self.conn.get(NextPleaseController.RowClass)
        self.assertEqual(0, len(rows))


    def test_processUpdateRevert(self):

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "записаться"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("Сообщите фамилию пациента", resp_text)
        rows = self.conn.get(NextPleaseController.RowClass)
        self.assertEqual(1, len(rows))
        self.assertEqual(308634083, rows[0].chat_id)

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "Сургуч"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("Укажите контактный телефон", resp_text)
        rows = self.conn.get(NextPleaseController.RowClass)
        self.assertEqual(1, len(rows))
        print(rows[0])
        self.assertEqual('Сургуч', rows[0].name)

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "+792632231575"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("Выберете дату", resp_text)
        rows = self.conn.get(NextPleaseController.RowClass)
        self.assertEqual(1, len(rows))
        print(rows[0])
        self.assertEqual(792632231575, rows[0].phone)

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "back"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("Укажите контактный телефон", resp_text)
        rows = self.conn.get(NextPleaseController.RowClass)
        self.assertEqual(1, len(rows))
        print(rows[0])
        self.assertEqual(None, rows[0].phone)


    def test_processUpdateCancel(self):

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "записаться"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("Сообщите фамилию пациента", resp_text)
        rows = self.conn.get(NextPleaseController.RowClass)
        self.assertEqual(1, len(rows))
        self.assertEqual(308634083, rows[0].chat_id)

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "cancel"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("Запись отменена", resp_text)
        rows = self.conn.get(NextPleaseController.RowClass)
        self.assertEqual(0, len(rows))


    def test_selectDates_dates(self):

        RowClass = getRow('slots', ['date', 'time', 'free'])
        row = RowClass(date=datetime(2021, 1, 12).timestamp(), time=13 * 60 * 60, free=True)
        dates = SelectDate.selectDates(row)
        self.assertEqual(1, len(dates))


    def test_selectDates_time(self):
        RowClass = getRow('slots', ['date', 'time', 'free'])
        row = RowClass(date=datetime(2021, 1, 12).timestamp(), time=13 * 60 * 60, free=True)
        times = SelectDate.selectTime(row)
        self.assertEqual(8, len(times))


    def test_review(self):

        row = self.RowClass(chat_id=308634083, name='Ivanov', phone=79263231575, date=datetime(2021, 1, 12).timestamp(),
                            time=13 * 60 * 60, complete=True)
        self.conn.put(row)
        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "review"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("308634083\nIvanov\n+7(926)323-15-75\n12-01-2021\n13:00\n1", resp_text)


    def test_review_absent(self):

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "review"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("У Вас нет ни одной предстоящей записи", resp_text)


    def test_delete(self):

        row = self.RowClass(chat_id=308634083, name='Ivanov', phone=79263231575, date=datetime(2021, 1, 12).timestamp(),
                            time=13 * 60 * 60, complete=True)
        self.conn.put(row)
        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "delete"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("Удалена ближайшая запись:\n308634083\nIvanov\n+7(926)323-15-75\n12-01-2021\n13:00\n1", resp_text)
        rows = self.conn.get(self.RowClass)
        self.assertEqual(0, len(rows))


    def test_delete_absent(self):

        update = {"update_id": 535230332, "message": {"message_id": 2045, "from": {"id": 308634083, "is_bot": False,
                                                                                   "first_name": "Vladimir",
                                                                                   "username": "YouCube",
                                                                                   "language_code": "en"},
                                                      "chat": {"id": 308634083, "first_name": "Vladimir",
                                                               "username": "YouCube", "type": "private"},
                                                      "date": 1588075894, "text": "delete"}}
        resp_text = processUpdate(update, fake=True)
        self.assertEqual("У Вас нет ни одной предстоящей записи", resp_text)


