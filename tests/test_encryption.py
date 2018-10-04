#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-
import base64
from unittest import TestCase

from app.ws.communication_data import EncryptMessage

test_key = base64.b64decode("ypc677QsEsfGepH8B1XAwfS4YF4bywuHYUtks/0Nodo=")


class TestEncryption(TestCase):
    def test_encryption(self):
        enc = EncryptMessage('applicationtest')
        print(enc.get_payload())

class TestDecryption(TestCase):
    print("test")

