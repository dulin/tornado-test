#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-
import json
import time
import uuid


class OutgoingConfigCheckMessage():
    def generate(self):
        uid = str(uuid.uuid4())
        t = int(time.time())
        command = 'echo "getConfigCheck"; md5sum /tmp/running.cfg | cut -d" " -f1'
        data = {
            "id": uid,
            "socket": "sys",
            "type": "rpc",
            "name": "cmd",
            "timestamp": t,
            "request": command,
            "protocol": "2.0"
        }
        output = {
            "payload": json.dumps(data, sort_keys=True, ensure_ascii=False),
            "meta": {},
            "original": data
        }

        return output
