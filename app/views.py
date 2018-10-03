#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-

from tornado.web import RequestHandler

class HelloWorld(RequestHandler):

    def get(self):
        self.write("Hello :)")