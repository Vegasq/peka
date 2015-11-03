__author__ = 'vegasq'
import requests
import re
import sqlite3
import time
import base64


chat_url = "http://chat.sc2tv.ru/memfs/channel-moderator.json"
url_finder = re.compile('\[url=.*\](.*?)\[/url\]', re.IGNORECASE)
allowed_types = [
    'image/jpeg', 'image/png', 'image/gif'
]


class DB(object):
    def __init__(self):
        self.conn = sqlite3.connect('p3ka.db')
        self.c = self.conn.cursor()

        try:
            self.c.execute('''CREATE TABLE messages
                           (date int, name text, url text, url64 text)''')
        except sqlite3.OperationalError as e:
            if str(e) != 'table messages already exists':
                raise sqlite3.OperationalError(e)

    def add(self, message):
        print('add message')
        if self.is_exist(message):
            return
        self.c.execute(
            "INSERT INTO messages VALUES (?, ?, ?, ?)", (
                int(time.time()),
                message['name'],
                message['message'],
                base64.b64encode(message['message']))
        )
        self.conn.commit()

    def is_exist(self, message):
        t = (message['name'], message['message'])
        self.c.execute('SELECT * FROM messages WHERE name=? AND url=?', t)
        if self.c.fetchone():
            return True
        return False


class Chat(object):
    def __init__(self):
        self.db = DB()

    def get_chat(self):
        # Get chat feed from sc2tv
        try:
            data = requests.get(chat_url).json()["messages"]
        except (
            ValueError,
            requests.exceptions.ConnectionError
        ):
            print("# BANNED FROM SC2TV?")
            return

        for message in data:
            if (
                url_finder.findall(message['message']) and not
                self.db.is_exist({
                    'message': url_finder.findall(message['message'])[0],
                    'name': message['name']})
            ):
                # Read image headers and handle access exceptions
                try:
                    headers = requests.head(
                        url_finder.findall(message['message'])[0]
                    ).headers
                except (requests.ConnectionError,
                        requests.exceptions.MissingSchema,
                        requests.exceptions.InvalidSchema) as e:
                    continue

                # Validate image headers
                if (
                    'content-type' in headers and
                    headers['content-type'] not in allowed_types or
                    'content-length' in headers and
                    'content-length' in headers and
                    int(headers['content-length']) > 1000000 or
                    'content-length' in headers and
                    'content-length' in headers and
                    int(headers['content-length']) < 10000
                ):
                    continue

                self.db.add({
                    'name': message['name'],
                    'message': url_finder.findall(message['message'])[0]
                })


def run_watcher():
    chat = Chat()
    while True:
        chat.get_chat()
        time.sleep(1)
