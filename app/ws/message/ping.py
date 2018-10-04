#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-
import uuid
import time

class OutgoingPingMessage():
    """
    Temporarily to see how the things going on debug
    """
    def generate(self):

        uid = str(uuid.uuid4())
        t = int(time.time())

        output = {
            "payload": {
                "id": uid,
                "socket": "sys",
                "type": "rpc",
                "name": "ping",
                "timestamp": t,
                "request": {},
                "protocol": "2.0"
            },
            "meta": {},
            "original":
                {
                    "id": uid,
                    "socket": "sys",
                    "type": "rpc",
                    "name": "ping",
                    "timestamp": t,
                    "request": {},
                    "protocol": "2.0"
                }
        }

        return output
