__author__ = 'vegasq'

import sqlite3
import jinja2


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
            result.append({
                'date': item[0],
                'name': item[1],
                'url': item[2],
                'url64': item[3]
            })
        return result


class Index(object):
    slice_size = 20

    def __init__(self):
        self.db = DB()

    def build(self):
        all_posts = self.db.get_objects()
        total_posts = len(all_posts)
        pages = abs(total_posts / self.slice_size)
        template = jinja2.Template(open('template.html', 'r').read())

        i = 0
        while i < pages:
            with open('/root/p3ka/site/index%s.html' % i, 'w') as fl:
                fl.write(template.render(
                    data=all_posts[i * self.slice_size:
                                   i * self.slice_size + self.slice_size],
                    pages=range(0, total_posts)
                ))
            i += 1


def run_creator():
    creator = Index()
    while True:
        creator.build()
