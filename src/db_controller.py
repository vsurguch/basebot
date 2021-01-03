
from os import path

from ..config import DB_FILENAME
from .utils import sendMsg
from .dbutils import SqliteConnect, getRow
from .parse_utils import getNextToken, convertDateStr, convertTimeStr
from .plain_controller import PlainController


ERROR_TEXT = "Text is missing; provide <command>(e.g. add) <date> {op: <time>} <text>"
ERROR_DATE = "Invalid date; provide <date> in format dd-mm-yyyy"
ERROR_FORMAT = "Incomplete request; provide <command>(e.g. add) <date> {op: <time>} <text>"


def parse_msg(string):

    date_str, rest = getNextToken(string)
    date = convertDateStr(date_str)
    if (date is not None):
        date_ts = date.timestamp()
        time_str, rest = getNextToken(rest)
        if time_str:
            time = convertTimeStr(time_str)
            if time is not None:
                time_ts = time.total_seconds()
                if rest:
                    text = rest
                else:
                    raise ValueError(ERROR_TEXT)
            else:
                time_ts = 0
                text = time_str + ' ' + rest
            important = True if text.find("!") != -1 else False
            return date_ts, time_ts, text, important

        else:
            raise ValueError(ERROR_TEXT)
    else:
        raise ValueError(ERROR_DATE)


class DBController(PlainController):

    db_filename = path.join(path.dirname(__file__), DB_FILENAME)
    connection = SqliteConnect(db_filename)
    RowClass = getRow('reminder',
                      ['chat_id', 'date', 'time', 'text', 'important'])

    @classmethod
    def init(cls):
        pass

    @classmethod
    def process(cls, chat_id, msg_text):

        action, rest = getNextToken(msg_text)

        if (action == 'add' or action == 'Add') and rest:
            try:
                date_ts, time_ts, text, important = parse_msg(rest)
                row = cls.RowClass(chat_id=int(chat_id), date=date_ts, time=time_ts, text=text, important=important)
                cls.connection.put(row)
                result = "ok"
            except ValueError as ve:
                result = str(ve)
            except Exception as e:
                result = str(e)

        else:
            result = ERROR_FORMAT

        resp = sendMsg({'chat_id': chat_id, 'text': result})

        return resp.text






