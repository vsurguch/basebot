import unittest
from datetime import datetime, timedelta

from ..src.parse_utils import convertDateStr, convertDate, \
    convertTimeStr, convertTime, \
    getNextToken, \
    convertPhoneStr, convertPhone


class TestParseUtils(unittest.TestCase):

    def test_getNextToken(self):
        string = "add 21.12.2021 bla bla bla"
        token, rest = getNextToken(string)
        self.assertEqual("add", token)
        self.assertEqual("21.12.2021 bla bla bla", rest)

    def test_getNextToken2(self):
        string = ""
        token, rest = getNextToken(string)
        self.assertEqual('', token)
        self.assertEqual('', rest)


    def test_convertDateStr(self):
        string = "01.01.2021"
        date = convertDateStr(string)
        self.assertEqual(datetime(2021, 1, 1).timestamp(), date)

        string = "1/12/2021"
        date = convertDateStr(string)
        self.assertEqual(datetime(2021, 12, 1).timestamp(), date)


    def test_convertDate(self):
        d = datetime(day=7, month=1, year=1949).timestamp()
        self.assertEqual("07-01-1949", convertDate(d))


    def test_convertTimeStr(self):
        string = "21:20"
        t = convertTimeStr(string)
        self.assertEqual(timedelta(hours=21, minutes=20).total_seconds(), t)


    def test_convertTime(self):
        t = 60 * 20 + 60 * 60 * 20
        ts = convertTime(t)
        self.assertEqual("20:20", ts)


    def test_both(self):
        string = "01.01.2021"
        date = convertDateStr(string)
        string = "21:20"
        t = convertTimeStr(string)
        date += timedelta(seconds=t).total_seconds()
        self.assertEqual(datetime(2021, 1, 1, 21, 20).timestamp(), date)


    def test_convertPhoneStr(self):
        phone_str = '+7(926)3231575'
        phone = convertPhoneStr(phone_str)
        self.assertEqual(79263231575, phone)


    def test_convertPhone(self):
        phone = 79263231575
        phone_str = convertPhone(phone)
        self.assertEqual('+7(926)323-15-75', phone_str)



if __name__ == '__main__':
    unittest.main()