
from threading import Thread
from .utils import sendMsg


class PlainController(object):

    @classmethod
    def process(cls, chat_id, msg_text):
        #        keyboard = {'keyboard':[['Записать на операцию',], ['Список операций',]], 'resize_keyboard': True, 'one_time_keyboard': False}
        reply = {'chat_id': chat_id, 'text': msg_text}
        resp = sendMsg(reply)
        return resp.text

    @classmethod
    def processThreading(cls, chat_id, msg_text):
        thread = Thread(target=cls.process, args=(chat_id, msg_text), daemon=False)
        thread.start()
        return "Processing started in separate thread"
