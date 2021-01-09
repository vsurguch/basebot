
from os import path
from datetime import datetime
from ..config import INSTANCE
from .dialog_controller import DialogController
from .dbutils import getRow, SqliteConnect
from .utils import sendMsg
from .parse_utils import convertDateStr, convertTimeStr, convertPhoneStr, convertDate, convertTime, convertPhone
from .sql_comapision_enum import Comparision

DB_NAME = "data/nextplease.sqlite"

class SelectDate:

    RowClass = getRow('slots',
                      ['date', 'time', 'free'])
    conn_slots = SqliteConnect(path.join(INSTANCE, DB_NAME))

    @classmethod
    def selectDates(cls, row):

        rows = cls.conn_slots.get(cls.RowClass, _order='date', date=(Comparision.MoreEqual, int(datetime.today().timestamp())), free=True)
        result_dict = {}

        for row in rows:
            if row.date not in result_dict:
                result_dict[row.date] = [row.time,]
            else:
                result_dict[row.date].append(row.time)

        lines = [f"{convertDate(d)} ({len(slots)} свободно)" for d,slots in result_dict.items()]
        return lines


    @classmethod
    def selectTime(cls, row):
        rows = cls.conn_slots.get(cls.RowClass, _order='time', date=row.date, free=True)
        lines = [convertTime(row.time) for row in rows]
        return lines




class NextPleaseController(DialogController):

    ROW_FIELDS = ['chat_id', 'name', 'phone', 'date', 'time', 'complete']
    FIELD_PROMPTS = {'name': "Сообщите фамилию пациента",
                     'phone': 'Укажите контактный телефон',
                     'date': 'Выберете дату',
                     'time': 'и время'}
    VALIDATORS = {'date': convertDateStr,
                  'time': convertTimeStr,
                  'phone': convertPhoneStr}
    CONVERTERS = {'date' : convertDate,
                    'time': convertTime,
                  'phone': convertPhone}
    RowClass = getRow("appointments", ROW_FIELDS)
    connection = SqliteConnect(path.join(INSTANCE, DB_NAME))


    SUBQUERIES = {'date': SelectDate.selectDates,
                  'time': SelectDate.selectTime}

    # DB_NAME_IP = "data/inprogress.sqlite"
    # RowClassIP = getRow("inprogress", ['chat_id', 'json_data'])
    # connection_ip = SqliteConnect(path.join(INSTANCE, DB_NAME_IP))


    @classmethod
    def process(cls, chat_id, msg_text, cmd="", fake=False):

        result = "-"
        keyboard = None
        if cmd in ('add', 'back', 'cancel', ''):

            result = "Сначала необходимо начать новую запись"
            rows = cls.connection.get(cls.RowClass, chat_id=int(chat_id), complete=False)

            if len(rows) == 0 and cmd == 'add':
                try:
                    row = cls.RowClass(chat_id=int(chat_id), complete=False)
                    cls.connection.put(row)
                    next0, _ = cls.getNextNone(row)
                    result = cls.FIELD_PROMPTS[next0] if next0 is not None else 'Ошибка'
                except Exception as e:
                    result = str(e)

            elif len(rows) != 0:
                try:
                    if cmd == 'back':
                        last = cls.getLastNotNone(rows[-1])
                        cls.revert(rows[-1], last)
                        result = cls.FIELD_PROMPTS[last]

                    elif cmd == 'cancel':
                        cls.connection.delete(rows[-1])
                        result = 'Запись отменена'

                    elif cmd == '':
                        next0, next1 = cls.getNextNone(rows[-1])
                        if next0 is not None:
                            validated = msg_text if cls.VALIDATORS.get(next0) is None else cls.VALIDATORS[next0](msg_text)
                            if validated is not None:
                                complete = True if next1 is None else False
                                modify = {next0: validated, 'complete': complete}
                                row = cls.connection.modify(rows[-1], **modify)
                                if complete:
                                    result = 'ok'
                                else:
                                    result = cls.FIELD_PROMPTS[next1]
                                    if next1 in cls.SUBQUERIES:
                                        keyboard = cls.SUBQUERIES[next1](row)
                            else:
                                result = "wrong format. " + cls.FIELD_PROMPTS[next0]

                except Exception as e:
                    result = str(e)

        elif cmd  in ('review', 'delete'):
            result = "У Вас нет ни одной предстоящей записи"
            rows = cls.connection.get(cls.RowClass, _order='date',
                                      chat_id=int(chat_id),
                                      complete=True,
                                      date=(Comparision.MoreEqual, int(datetime.today().timestamp())))

            if len(rows) > 0:
                result = '\n'.join(map(str, cls.convertRowToStrList(rows[0], add_fields=False)[1:-1]))

                if cmd == 'delete':
                    cls.connection.delete(rows[0])
                    result = f"Удалена ближайшая запись:\n{result}"
                else:
                    result = f"Ваша ближайшая запись:\n{result}"

        if fake:
            resp = result
        else:
            resp = sendMsg(chat_id, result, keyboard).text

        return resp


