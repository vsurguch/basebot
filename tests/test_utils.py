import json
import unittest


from ..src.utils import make_request_json, sendMsg, sendPhoto, \
    downloadAndSaveFile, getFileLink, getFileInfo, FileInfo


url = "http://127.0.0.1:5000/bot/"


class TestUtils(unittest.TestCase):

    def test_make_request_json(self):
        command = 'sendMessage'
        body = {
            'chat_id': '308634083',
            'text': 'Just testing...'
        }
        resp = make_request_json(command, body)
        self.assertTrue(resp.json()['ok'])

    def test_sendMsg(self):
        msg = {'chat_id': '308634083',
               'text': 'image'}
        resp = sendMsg(msg['chat_id'], msg['text'], None)
        self.assertTrue(resp.json()['ok'])


    def test_sendPhoto(self):
        msg = {'chat_id' : '308634083',
               'text': 'image'}
        filename = '/Users/vsurguch/Downloads/transformed.jpg'
        resp = sendPhoto(msg, filename)
        self.assertTrue(resp.json()['ok'])


    def test_getFileLink(self):
        file_id = 'AgACAgIAAxkBAAIICl9XlfaPDcz6q70OQPsFLBfyJpbyAAKOsDEbkIO4SkKvHHg6j6Ab64ZGli4AAwEAAwIAA3kAA4y7AQABGwQ'
        link = getFileLink(file_id)
        self.assertEqual(link, 'photos/file_40')

    def test_downloadAndSaveFile(self):
        filename = 'photos/file_40'
        loaded = downloadAndSaveFile(filename)
        self.assertTrue(loaded)

    def test_getFileInfo(self):
        sample = {'file_id': "123",
                  'name': "123.txt"}
        fileInfo = getFileInfo(sample)

        self.assertEqual(fileInfo, FileInfo(file_id="123", name="123.txt", caption=None))
