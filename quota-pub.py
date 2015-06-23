#!/usr/bin/env python
import os
import sys
import logging

from threading import Thread
from time import sleep

from quota_pub.quotapub import WebpyServer, ThreadMonitor

def main():

    tenant_list = {'test':1}
    threads = []
    # establishes ThreadMonitor and its thread
    monitor_thread = ThreadMonitor(tenant_list)
    monitor_thread.daemon = True
    threads.append(monitor_thread)

    # establishes WebpyServer and its thread
    webpy_thread = WebpyServer(tenant_list)
    webpy_thread.daemon = True
    threads.append(webpy_thread)

    # starts running threads
    for thread in threads:
        print "starting", thread
        thread.start()

    # keep running threads until KeyboardInterrupt
    try:
        while True:
            for thread in threads:
                if not thread.is_alive():
                    logging.error('{0} died.'.format(thread))
                    sys.exit()
            sleep(1)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    # sets up logging file
    #quota_dir = config.shoal_dir
    log_file = '/tmp/quotapub.log'
    log_format = '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)s] - %(message)s'

    try:
        logging.basicConfig(level=logging.ERROR, format=log_format, filename=log_file)
    except IOError as e:
        print "Could not set logger.", e
        sys.exit(1)

    main()
