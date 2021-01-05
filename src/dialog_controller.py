
from os import path
from ..config import INSTANCE
from .plain_controller import PlainController
from .dbutils import getRow, SqliteConnect
from .parse_utils import convertDateStr, convertTimeStr, convertPhoneStr, convertTime, convertPhone


class DialogController(PlainController):


    DB_NAME = "data/termin.sqlite"
    ROW_FIELDS = ['chat_id', 'name', 'date', 'time', 'phone', 'text', 'complete']
    FIELD_PROMPTS = {'name': "provide patients name",
                     'date': 'what date?',
                     'time': 'what time?',
                     'phone': 'provide patient\'s phone',
                     'text': 'additional info'}
    VALIDATORS = {'date': convertDateStr,
                  'time': convertTimeStr,
                  'phone': convertPhoneStr}
    CONVERTERS = {'time': convertTime,
                  'phone': convertPhone}
    RowClass = getRow("termin", ROW_FIELDS)
    connection = SqliteConnect(path.join(INSTANCE, DB_NAME))

    # DB_NAME_IP = "data/inprogress.sqlite"
    # RowClassIP = getRow("inprogress", ['chat_id', 'json_data'])
    # connection_ip = SqliteConnect(path.join(INSTANCE, DB_NAME_IP))


    @classmethod
    def getNextNone(cls, row):

        next0 = None
        next1 = None

        for field in cls.ROW_FIELDS:
            if getattr(row, field) is None:
                if next0 is None:
                    next0 = field
                elif next1 is None:
                    next1 = field
                else:
                    break

        return next0, next1


    @classmethod
    def convertRowToStr(cls, row):
        result = ''
        for field in cls.ROW_FIELDS[1: -1]:
            value = getattr(row, field)
            value = cls.CONVERTERS[field](value) if field in cls.CONVERTERS else value
            result += f"{field}: {value}; "
        return result[:-1]


    @classmethod
    def process(cls, chat_id, msg_text, cmd=""):

        result = "-"
        rows = cls.connection.get(cls.RowClass, chat_id=int(chat_id), complete=False)
        if len(rows) == 0 and cmd == 'add':
            try:
                row = cls.RowClass(chat_id=int(chat_id), complete=False)
                cls.connection.put(row)
                next0, _ = cls.getNextNone(row)
                result = cls.FIELD_PROMPTS[next0] if next0 is not None else 'unknown'
            except Exception as e:
                result = str(e)

        elif len(rows) != 0 and cmd == '':
            result = "unknown"
            next0, next1 = cls.getNextNone(rows[-1])
            # print(next0, next1)

            if next0 is not None:
                validated = msg_text if cls.VALIDATORS.get(next0) is None else cls.VALIDATORS[next0](msg_text)
                if validated is not None:
                    complete = True if next1 is None else False
                    modify = {next0: validated, 'complete': complete}
                    print(validated)
                    cls.connection.modify(rows[-1], **modify)
                    result = 'ok' if complete else cls.FIELD_PROMPTS[next1]
                else:
                    result = "wrong format. " + cls.FIELD_PROMPTS[next0]

        return result


