#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-

import logging
from tornado import gen
from tornado.websocket import WebSocketHandler, WebSocketClosedError
from tornado.queues import Queue
from .communication_data import ParseMessage
from .message.ping import OutgoingPingMessage

class CommunicationSocketHandler(WebSocketHandler):
    waiters = set()

    def initialize(self):
        self.messages = Queue()

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        logging.info("websocket open")
        CommunicationSocketHandler.waiters.add(self)

    def on_close(self):
        logging.info("websocket close")
        CommunicationSocketHandler.waiters.remove(self)
        self._close()

    def on_message(self, message):
        logging.info("got message %r", message)
        debug = ParseMessage(message.decode('utf-8'))
        logging.info("try parse message %s", str(debug.get_all_b64()))
        logging.info("Output: %s", debug.decrypt())
        out = OutgoingPingMessage()
        outSend = out.generate()
        logging.info("send message %r", outSend)
        self.send(outSend)

    def on_pong(self, data):
        """Invoked when the response to a ping frame is received."""
        logging.info("pong received")

    def on_ping(self, data):
        """Invoked when the a ping frame is received."""
        logging.info("ping received")


    def parse_message(self, message):
        """"""
        return {}

    def send(self, message):
        logging.info("trying send message")
        try:
            self.write_message(dict(value=message))
        except WebSocketClosedError:
            logging.info("socket closed error")
            self._close()

    def _close(self):
        self.finished = True

    @gen.coroutine
    def submit(self, message):
        yield self.messages.put(message)


    @gen.coroutine
    def run(self):
        logging.info("Run")
        while not self.finished:
            message = yield self.messages.get()
            print("New message: " + str(message))
            self.send(message)
