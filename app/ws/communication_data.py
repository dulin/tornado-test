#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-

import string
import base64
from Cryptodome import Random
from Cryptodome.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]
AES_KEY_LENGTH = 32


def unescape_b64(s):
    """
    Reverse base64-url
    """
    return (s + "=" * ((len(s) * -1) % 4)).translate(string.maketrans(b'-_', b'+/'))

def decode_base64(data):
    """
    Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return base64.decodestring(data)


class AESCipher:
    def __init__(self, key):
        """
        Requires hex encoded param as a key
        """
        self.key = key

    def encrypt(self, raw):
        """
        Returns hex encoded encrypted value!
        """
        raw = pad(raw)
        iv = Random.new().read(AES.block_size);
        cipher = AES.new(self.key, AES.MODE_GCM, iv)

        return (iv + cipher.encrypt(raw)).encode("hex")

    def decrypt(self, enc, iv):
        """
        Requires hex encoded param to decrypt
        """
        cipher = AES.new(self.key, AES.MODE_GCM, iv)
        return unpad(cipher.decrypt(enc))


class ParseMessage:
    iv = ""
    auth_tag = ""
    AES_KEY_LEN = 32
    IV_LEN = 22
    AUTH_TAG_LEN = 22
    MAC_LEN = 8
    MIN_MESSAGE_LEN = IV_LEN + AUTH_TAG_LEN + MAC_LEN
    devel_key = base64.b64decode("ypc677QsEsfGepH8B1XAwfS4YF4bywuHYUtks/0Nodo=")

    def __init__(self, encrypted_message, first_time=False):
        unescaped_message = unescape_b64(str(encrypted_message))
        self.iv = decode_base64(unescaped_message[:self.IV_LEN])
        self.auth_tag = decode_base64(unescaped_message[self.IV_LEN:self.AUTH_TAG_LEN])
        self.mac = decode_base64(unescaped_message[self.IV_LEN + self.AUTH_TAG_LEN:self.MAC_LEN])
        self.encrypted = decode_base64(unescaped_message[self.MIN_MESSAGE_LEN:])

    def get_all(self):
        return {'iv': self.iv, 'authTag': self.auth_tag, 'mac': self.mac, 'encryptedMessage': self.encrypted }

    def get_all_b64(self):
        return {
            'iv': base64.b64encode(self.iv),
            'authTag': base64.b64encode(self.auth_tag),
            'mac': base64.b64encode(self.mac),
            'encryptedMessage': base64.b64encode(self.encrypted)
        }

    def get_iv(self):
        return self.iv

    def get_auth_tag(self):
        return self.auth_tag

    def decrypt(self):
        dec = AESCipher(self.devel_key)
        return dec.decrypt(self.encrypted, self.iv)






