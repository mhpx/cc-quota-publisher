#!/usr/bin/env python
import sys
import os
import web
import json
import urllib
import logging
import socket
import uuid

from time import time, sleep
from threading import Thread




"""
    Main application that will monitor TenantUpdate threads.
"""
class ThreadMonitor(Thread):

    def __init__(self, tenants):
        """
        constructor for ThreadMonitor, sets up threads and tracks health
        """

        Thread.__init__(self)

        self.tenants = tenants
        self.threads = []

        update_thread = TenantUpdate(self.tenants)
        update_thread.daemon = True
        self.threads.append(update_thread)


    def run(self):
        """
        runs ThreadMonitor threads
        """
        for thread in self.threads:
            logging.info("starting", thread)
            thread.start()
        while True:
            for thread in self.threads:
                if not thread.is_alive():
                    logging.error('{0} died. Stopping application...'.format(thread))
                    sys.exit(1)
            sleep(1)

    def stop(self):
        """
        stops ThreadMonitor threads
        """
        logging.info("Shutting down QuotaPub-Server... Please wait.")
        try:
            self.update.stop()
        except Exception as e:
            logging.error(e)
            sys.exit(1)
        finally:
            sleep(2)
        sys.exit()

"""
    TenantUpdate is used for updating the tenant quota list every set interval.
"""
class TenantUpdate(Thread):

    INTERVAL = 30
    INACTIVE = 15

    def __init__(self, tenants):
        """TenantUpdate
        constructor for TenantUpdate, uses parent Thread constructor as well
        """
        Thread.__init__(self)
        self.tenants = tenants
        self.running = False

    def run(self):
        """
        runs TenantUpdate
        """
        self.running = True
        while self.running:
            sleep(self.INTERVAL)
            self.update()

    def update(self):
        """
        updates tenant quota list - this is where will read in a file or something
        """
        for tenant in self.tenants.keys():
            self.tenants[tenant] += 1

    def stop(self):
        """
        stops TenantUpdate
        """
        self.running = False

"""
    Webpy webserver used to serve up tenant quotas and API calls. Can run as either the development server or under mod_wsgi.
"""
class WebpyServer(Thread):

    def __init__(self, tenants):
        """
        constructor for WebpyServer, uses parent Thread constructor as well.
        """
        Thread.__init__(self)
        web.tenants = tenants
        web.config.debug = False
        self.app = None
        self.urls = (
            '/all/?(\d+)?/?', 'quota_pub.view.alltenants',
            '/tenant/(.*)', 'quota_pub.view.tenant',
            '/(\d+)?/?', 'quota_pub.view.index',
        )

    def run(self):
        """
        runs web application
        """
        try:
            self.app = web.application(self.urls, globals())
            self.app.run()
        except Exception as e:
            logging.error("Could not start webpy server.\n{0}".format(e))
            sys.exit(1)

    def wsgi(self):
        """
        returns Web Server Gateway Interface for application
        """
        return web.application(self.urls, globals()).wsgifunc()

    def stop(self):
        """
        stops web application
        """
        self.app.stop()

