
from os import path
from ..config import INSTANCE
from .utils import sendMsg
from .plain_controller import PlainController
from .dbutils import getRow, SqliteConnect
from .parse_utils import convertDateStr, convertTimeStr, convertPhoneStr, convertDate, convertTime, convertPhone


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
    CONVERTERS = {'date': convertDate,
                    'time': convertTime,
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
    def getLastNotNone(cls, row):
        last = None
        for i in range(len(cls.ROW_FIELDS)):
            if (getattr(row, cls.ROW_FIELDS[i]) is not None) \
                    and (i < len(cls.ROW_FIELDS)-1) \
                    and (getattr(row, cls.ROW_FIELDS[i+1]) is None):
                last = cls.ROW_FIELDS[i]
                break

        return last


    @classmethod
    def revert(cls, row, field):
        cls.connection.modify(row, **{field: None})


    @classmethod
    def convertRowToStrList(cls, row, add_fields=True):
        result = list()
        for field in cls.ROW_FIELDS:
            value = getattr(row, field)
            value = cls.CONVERTERS[field](value) if field in cls.CONVERTERS else value
            value = f"{field}: {value}" if add_fields else value
            result.append(value)
        return result


    @classmethod
    def process(cls, chat_id, msg_text, cmd="", fake=False):

        result = "-"
        keyboard = None
        rows = cls.connection.get(cls.RowClass, chat_id=int(chat_id), complete=False)
        if len(rows) == 0 and cmd == 'add':
            try:
                row = cls.RowClass(chat_id=int(chat_id), complete=False)
                cls.connection.put(row)
                next0, _ = cls.getNextNone(row)
                result = cls.FIELD_PROMPTS[next0] if next0 is not None else 'Error'
            except Exception as e:
                result = str(e)

        elif len(rows) != 0 and cmd == '':
            result = "Error"
            next0, next1 = cls.getNextNone(rows[-1])

            if next0 is not None:
                validated = msg_text if cls.VALIDATORS.get(next0) is None else cls.VALIDATORS[next0](msg_text)
                if validated is not None:
                    complete = True if next1 is None else False
                    modify = {next0: validated, 'complete': complete}
                    cls.connection.modify(rows[-1], **modify)
                    result = 'ok' if complete else cls.FIELD_PROMPTS[next1]
                else:
                    result = "wrong format. " + cls.FIELD_PROMPTS[next0]

        if fake:
            resp = result
        else:
            resp = sendMsg(chat_id, result, keyboard).text

        return resp


