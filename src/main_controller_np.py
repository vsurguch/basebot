
import json

from flask import current_app
from .utils import *
from .np_controller import NextPleaseController
from .parse_utils import getNextToken


MAKE_APPOINTMENT = ('записаться', 'запись', '/записаться')
BACK_COMMAND = ('back', '/back', 'назад', 'вернуться')
CANCEL_COMMAND = ('cancel', '/cancel', 'отменить')
REVIEW_COMMAND = ('review', '/review', 'просмотреть')
DELETE_COMMAND = ('delete', '/delete', 'удалить')

def processUpdate(update, fake=False):
    log(f'new update from: {json.dumps(update)}\n')
    sender_id = update['message']['from']['id']
    sender_name = update['message']['from']['username']
    chat_id = update['message']['chat']['id']
    text = update['message']['text'] if 'text' in update['message'] else ''
    cmd, rest = getNextToken(text)

    # text = update['message']['edited_text'] if not text and 'edited_text' in update['message'] else ''

    cmd_ = cmd.lower().strip()
    if cmd_ in MAKE_APPOINTMENT:
        cmd = "add"
    elif cmd_ in BACK_COMMAND:
        cmd = "back"
    elif cmd_ in CANCEL_COMMAND:
        cmd = "cancel"
    elif cmd_ in REVIEW_COMMAND:
        cmd = "review"
    elif cmd_ in DELETE_COMMAND:
        cmd = "delete"
    else:
        rest = " " + rest if rest else ""
        rest = cmd + rest
        cmd = ""

    if fake:
        resp_text = NextPleaseController.process(chat_id, rest, cmd=cmd, fake=fake)
    else:
        resp_text = NextPleaseController.processThreading(chat_id, rest, cmd=cmd)

    log(f"Resp message from controller: {resp_text}")

    return resp_text