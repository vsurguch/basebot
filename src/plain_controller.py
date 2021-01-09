
import json
from threading import Thread
from .utils import sendMsg


class PlainController(object):

    @classmethod
    def process(cls, chat_id, msg_text, cmd="", fake=False):
        keyboard = None
        #        keyboard = {'keyboard':[['Записать на операцию',], ['Список операций',]], 'resize_keyboard': True, 'one_time_keyboard': False}
        reply = {'chat_id': chat_id, 'text': msg_text, 'keyboard': keyboard}
        if fake:
            resp = msg_text
        else:
            resp = sendMsg(chat_id, msg_text, keyboard).text
        return resp

    @classmethod
    def processThreading(cls, chat_id, msg_text, cmd="", fake=False):
        thread = Thread(target=cls.process, args=(chat_id, msg_text, cmd, fake), daemon=False)
        thread.start()
        return "Processing started in separate thread"
