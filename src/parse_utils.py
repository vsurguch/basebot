
import re
from datetime import datetime, timedelta

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
            date = datetime(year=int(y), month=int(m), day=int(d))
        except Exception:
            date = None
        return date

    return None


def convertTimeStr(string):

    match = re.match("(\d{1,2})[\:\-](\d{1,2})",
                     string.lstrip())
    if match is not None:
        h = int(match.group(1))
        m = int(match.group(2))
        h = h if (h > 0 and h < 24) else 0
        m = m if (m > 0 and  m < 60) else 0
        return timedelta(hours=h, minutes=m)
    return None