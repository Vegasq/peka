#!/usr/bin/python3
import os
import logging
from multiprocessing import Process

from watcher import run_watcher
from creator import run_creator

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT)
LOG = logging.getLogger('tcpserver')

# docker run  -i -t -v /usr/share/nginx/html/:/root/p3ka/site p3ka /usr/bin/python /root/p3ka/p3ka.py

if __name__ == '__main__':
    try:
        os.chdir('/root/p3ka/')
    except OSError:
        LOG.debug('Can\'t change dir')

    p = Process(target=run_creator)
    p.start()
    # p.join()

    p = Process(target=run_watcher)
    p.start()
    # p.join()
