
from collections import namedtuple
from os import path
import requests

# from . import config
# from .log import log
from .. import config
from .log import log


url_base = 'https://api.telegram.org/'
token = config.TOKEN
FileInfo = namedtuple("FileInfo", ["file_id", "name", "caption"])


def make_request_simple(command):
    url = f'{url_base}bot{token}/{command}'
    return requests.get(url)


def make_request_json(command, body, files=None):
    url = f'{url_base}bot{token}/{command}'

    if files is None:
        headers = { 'Content-type': 'application/json' }
        resp = requests.post(url, headers=headers, json=body)
    else:
        resp = requests.post(url, data=body, files=files)

    return resp


# def sendMsg(msg):
#     body = {
#         'chat_id': msg['chat_id'],
#         'text': msg["text"]
#     }
#
#     if 'keyboard' in msg:
#         body['reply_markup'] = msg['keyboard']
#
#     command = 'sendMessage'
#     resp = make_request_json(command, body)
#     log(f"server reply to answer: {resp.text}")
#     return resp


def sendMsg(chat_id, text, keyboard):
    body = {
        'chat_id': chat_id,
        'text': text
    }

    if keyboard is not None:
        body['reply_markup'] = keyboard

    command = 'sendMessage'
    resp = make_request_json(command, body)
    log(f"server reply to answer: {resp.text}")
    return resp


def sendPhoto(msg, filepath):
    body = {'chat_id': msg['chat_id'],
            'caption': msg["text"], }

    # filepath = path.join(current_app.config['INSTANCE'], 'downloads', filename)
    fp = open(filepath, 'rb')
    files = {'photo': fp}
    resp = make_request_json('sendPhoto', body, files=files)
    log(f"server reply to answer: {resp.text}")
    fp.close()
    return resp

def getFileInfo(data):
    return FileInfo(file_id=data.get('file_id'),
                    name=data.get('name'),
                    caption=data.get('caption'))


def getFileLink(file_id):
    command = 'getFile'
    body = { 'file_id': file_id }
    resp = make_request_json(command, body)
    link = ''
    if resp.status_code == 200:
        try:
            resp = resp.json()
            if resp['ok']:
                link = resp['result']['file_path']
        except ValueError:
            pass
    return link


def createFileName(name):
    downloads_path = path.join(config.INSTANCE, 'downloads')
    with open(path.join(downloads_path, 'last_id.txt'), 'r') as f:
        id = int(f.read())
    with open(path.join(downloads_path, 'last_id.txt'), 'w') as f:
        f.write(str(id+1))
    filename = f'doc{id}.jpg' if name is None else f"doc{id}_{name}"

    return path.join(downloads_path, filename)


def downloadAndSaveFile(file_path, name='img.jpg'):
    loaded = False
    url = f'{url_base}file/bot{token}/{file_path}'
    try:
        resp = requests.get(url)
        if (resp.status_code == 200):
            with open(name, 'wb') as f:
                f.write(resp.content)
            log(f'file {file_path} downloaded and read')
            loaded = True
    except Exception as e:
        log(f'Exception while downloading and reading file. {e}')

    return loaded

def processAttachments(message):
    credentials = None
    if 'photo' in message:
        credentials = getFileInfo(message['photo'][-1])
    if 'document' in message:
        credentials = getFileInfo(message['document'])
    if credentials is not None:
        log(f'credentials = {credentials}')
        link = getFileLink(credentials.file_id)
        log(f'link = {link}')
        if link:
            name = createFileName(credentials.name)
            downloadAndSaveFile(link, name)