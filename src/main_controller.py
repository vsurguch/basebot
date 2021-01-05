
import json

from flask import current_app
from .utils import *
from .plain_controller import PlainController
from .weather_controller import WeatherContoller
from .db_controller import DBController


# from .utils import *
# from .plain_controller import PlainController
# from .weather_controller import WeatherContoller


def access_denied(chat):
    return sendMsg({'chat_id': chat,
             'text': 'Access denied', })


def processUpdate(update, fake=False):
    log(f'new update from: {json.dumps(update)}\n')
    sender_id = update['message']['from']['id']
    sender_name = update['message']['from']['username']
    chat_id = update['message']['chat']['id']
    text = update['message']['text'] if 'text' in update['message'] else ''
    cmd, _, rest = text.partition(" ")
    cmd = cmd.lower().strip()
    # text = update['message']['edited_text'] if not text and 'edited_text' in update['message'] else ''

    if fake:
        log(f"processed msg : {json.dumps(update)}")
        return "ok"

    if sender_id not in current_app.config['USERS']:
        access_denied(chat_id)
        resp_text = "access denied"
    else:
        if cmd == "pogoda" or cmd == "weather":
            resp_text = WeatherContoller.processThreading(chat_id, rest)
        elif cmd == "remind":
            resp_text = DBController.processThreading(chat_id, rest)
        else:
            processAttachments(update['message'])
            resp_text = PlainController.processThreading(chat_id, text, cmd)
            # resp_text = "controller not found"
        log(f"Resp message from controller: {resp_text}")
    return resp_text