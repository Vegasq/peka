__author__ = 'vegasq'

import os
import sqlite3
import json
import jinja2
import time
from time import sleep

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

    def get(self, limit=1000):
        self.c.execute(
            "SELECT * FROM messages ORDER BY date DESC LIMIT %i" % limit)
        return self.c.fetchall()

    def get_objects(self, limit=1000):
        data = self.get(limit=limit)
        result = []
        for item in data:
            post = {
                'name': item[1].encode("utf-8"),
                'url': item[2].encode("utf-8")
            }

            if type(item[1]) == bytes:
                post['name'] = item[1].encode("utf-8")
            if type(item[2]) == bytes:
                post['url'] = item[2].encode("utf-8")

            result.append(post)

        return result


class Index(object):
    slice_size = 12
    path = '/root/p3ka/site/'

    last_url = ''

    def __init__(self):
        if not os.path.isdir(self.path):
            self.path = 'site/'

        self.db = DB()

    def build(self):
        all_posts = self.db.get_objects()

        if self.last_url == all_posts[0]['name']:
            print('No new messages')
            sleep(1)
            return
        else:
            print("New message found")
            self.last_url = all_posts[0]['name']

        print('Rebuild site')
        start_time = time.time()

        pages = int(abs(len(all_posts) / self.slice_size))
        template = jinja2.Template(open('template.html', 'r').read())

        for i in range(0, pages):
            with open('%sindex%s.html' % (self.path, i), 'w') as fl:
                posts_to_work = all_posts[i * self.slice_size:
                                          i * self.slice_size + self.slice_size]

                fl.write(template.render(
                    data=posts_to_work,
                    pages=range(0, pages)
                ))
                # hack to generate first page
                if i == 0:
                    with open('%sindex.html' % (self.path), 'w') as fl0:
                        fl0.write(template.render(
                            data=posts_to_work,
                            pages=range(0, pages)
                        ))

        print('Rebuild site done')
        print("--- %s seconds ---" % (time.time() - start_time))


def run_creator():
    creator = Index()
    while True:
        creator.build()
