#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-
import base64
import binascii
from unittest import TestCase

from app.ws.communication_data import EncryptMessage, DecryptMessage, b64escape, decode_base64

test_key = base64.b64decode("ypc677QsEsfGepH8B1XAwfS4YF4bywuHYUtks/0Nodo=")
test_iv = base64.b64decode("WhGwq9dYQuOi2EFXllH0/A==")
test_encoded = "WhGwq9dYQuOi2EFXllH0_AaLNH2GQwS7a8rH68KQGsVgttRPkZix59B1NwJcIyLB"


class TestCommunicationData(TestCase):
    def test_encryption(self):
        enc = EncryptMessage('applicationtest', test_key, test_iv)
        self.assertEqual(enc.get_payload(), test_encoded)

    def test_decryption(self):
        dec = DecryptMessage(test_encoded)
        self.assertEqual(dec.real_decryption(aes_key=test_key), b'applicationtest')

    def test_base64_incorrect_padding(self):
        b64 = base64.b64encode(b'applicationtest!').decode()
        b64_url = b64escape(b64)
        self.assertRaises(binascii.Error, base64.b64decode, b64_url)

    def test_base64_decode(self):
        b64 = b64escape(base64.b64encode(b'applicationtest!').decode())
        self.assertEqual(decode_base64(b64), b'applicationtest!')
