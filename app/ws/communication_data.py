#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- mode: python -*-

import base64
import json
import string
import uuid

from Cryptodome import Random
from Cryptodome.Cipher import AES

AES_KEY_LEN = 32
IV_LEN = 22
AUTH_TAG_LEN = 22
MAC_LEN = 8

MAC_START_LOC = IV_LEN + AUTH_TAG_LEN
MAC_END_LOC = IV_LEN + AUTH_TAG_LEN + MAC_LEN
AUTH_TAG_END = IV_LEN + AUTH_TAG_LEN
MIN_MESSAGE_LEN = IV_LEN + AUTH_TAG_LEN + MAC_LEN
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]
AES_KEY_LENGTH = 32


def b64escape(s):
    return s.replace('=', "").translate(string.maketrans(b'+/', b'-_'))


def b64unescape(s):
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
        data += b'=' * (4 - missing_padding)
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
        return cipher.decrypt(enc)


class DecryptMessage:
    devel_key = base64.b64decode("ypc677QsEsfGepH8B1XAwfS4YF4bywuHYUtks/0Nodo=")

    def __init__(self, encrypted_message, is_connect_message=False):
        self.unescaped_message = b64unescape(str(encrypted_message))
        self.iv = decode_base64(self.unescaped_message[:IV_LEN])
        self.auth_tag = decode_base64(self.unescaped_message[IV_LEN:AUTH_TAG_END])
        self.mac = ""
        self.encrypted = ""

        self.load_data(is_connect_message)

    def load_data(self, is_connect_message=False):
        if is_connect_message:
            self.mac = ""
            self.encrypted = decode_base64(self.unescaped_message[MAC_START_LOC:])
        else:
            self.mac = decode_base64(self.unescaped_message[MAC_START_LOC:MAC_END_LOC])
            self.encrypted = decode_base64(self.unescaped_message[MIN_MESSAGE_LEN:])

    def get_all(self):
        return {'iv': self.iv, 'authTag': self.auth_tag, 'mac': self.mac, 'encryptedMessage': self.encrypted}

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

    def real_decryption(self, aes_key=devel_key):
        dec = AESCipher(aes_key)
        return dec.decrypt(self.encrypted, self.iv)

    def decrypt(self, aes_key=devel_key):
        out = self.real_decryption(aes_key)
        try:
            json.loads(out)
        except ValueError:
            self.load_data(is_connect_message=True)
            out = self.real_decryption(aes_key)
            try:
                json.loads(out)
            except ValueError:
                raise Exception('Unable to decrypt message')

        return out


class EncryptMessage:
    devel_key = base64.b64decode("ypc677QsEsfGepH8B1XAwfS4YF4bywuHYUtks/0Nodo=")

    def __init__(self, message, aes_key=devel_key, iv=None):
        # similar to Random.get_random_bytes(16)
        if iv is None:
            self.iv = uuid.uuid4().bytes
        else:
            self.iv = iv
        cipher = AES.new(aes_key, AES.MODE_GCM, self.iv)
        self.ciphertext, self.auth_tag = cipher.encrypt_and_digest(message)

    def get_payload(self):
        payload = str(base64.b64encode(self.iv))
        payload += str(base64.b64encode(self.auth_tag))
        payload += str(base64.b64encode(self.ciphertext))
        return b64escape(payload)
