
import re
from datetime import datetime, timedelta, time

def getNextToken(string):
    nextToken, sep, rest = string.partition(" ")
    return nextToken, rest


def convertDateStr(string):

    match = re.match("(\d{1,2})[\.\/\-](\d{1,2})[\.\/\-](\d{4})",
                     string.lstrip())
    if match is not None:
        d = match.group(1)
        m = match.group(2)
        y = match.group(3)
        try:
            date = datetime(year=int(y), month=int(m), day=int(d)).timestamp()
        except Exception:
            date = None
        return date

    return None


def convertDate(d):
    return datetime.fromtimestamp(d).strftime("%d-%m-%Y")

def convertTimeStr(string):

    match = re.match("(\d{1,2})[\:\-](\d{1,2})",
                     string.lstrip())
    if match is not None:
        h = int(match.group(1))
        m = int(match.group(2))
        h = h if (h > 0 and h < 24) else 0
        m = m if (m > 0 and  m < 60) else 0
        return timedelta(hours=h, minutes=m).total_seconds()
    return None


def convertTime(t):
    h = int(t) // 3600
    m = (int(t) % 3600) // 60
    return time(hour=h, minute=m).strftime("%H:%M")


def convertPhoneStr(string):

    match = re.match("\+?(\d*)\(?(\d{3})\)?(\d{3})\-?(\d{2})\-?(\d{2})", string.lstrip())
    if match is not None:
        return int(match.group(1) + match.group(2) + match.group(3) + match.group(4) + match.group(5))
    return None


def convertPhone(phone):
    phone_str = str(phone)[::-1]
    new_phone_str = phone_str[0:2] \
                    + '-' + phone_str[2:4] \
                    + '-' + phone_str[4:7] \
                    + ')' + phone_str[7:10] \
                    + '(' + phone_str[10:]
    if new_phone_str[-1] == '7':
        new_phone_str += '+'
    new_phone_str = new_phone_str[::-1]
    return new_phone_str