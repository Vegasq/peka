#!/usr/bin/python
import os
from multiprocessing import Process

from watcher import run_watcher
from creator import run_creator


# docker run  -i -t -v /usr/share/nginx/html/:/root/p3ka/site p3ka /usr/bin/python /root/p3ka/p3ka.py

if __name__ == '__main__':
    os.chdir('/root/p3ka/')

    p = Process(target=run_creator)
    p.start()
    # p.join()

    p = Process(target=run_watcher)
    p.start()
    # p.join()
