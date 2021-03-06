#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-
import json
import time
import uuid


class OutgoingPingMessage():
    """
    Temporarily here to see how this go on debug
    """

    def generate(self):
        uid = str(uuid.uuid4())
        t = int(time.time())
        data = {
            "id": uid,
            "socket": "sys",
            "type": "rpc",
            "name": "ping",
            "timestamp": t,
            "request": {},
            "protocol": "2.0"
        }

        output = {
            "payload": json.dumps(data, sort_keys=True, ensure_ascii=False),
            "meta": {},
            "original": data
        }

        return output
