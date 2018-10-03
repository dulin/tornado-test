#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-

import os.path

import tornado.web

from app.views import HelloWorld
from app.ws.communication import CommunicationSocketHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HelloWorld),
            (r"//", CommunicationSocketHandler),
        ]
        settings = dict()
        super(Application, self).__init__(handlers, **settings)
