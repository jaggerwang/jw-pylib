import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES, ARC4
from Crypto.Hash import SHA


class AESCipher(object):
    """AES encrypt and decrypt.

    The encrypt result is a b64encoded string, easy to transfer.
    """

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode()

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])
                           ).decode('utf-8')

    def _pad(self, s):
        return (s + (self.bs - len(s) % self.bs) *
                chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


def aes_encode(data, key=b""):
    nonce = Random.new().read(4)
    tempkey = SHA.new(key + nonce).digest()
    cipher = ARC4.new(tempkey)
    data_bytes = data.encode('utf8')
    total_bytes = nonce + cipher.encrypt(data_bytes)
    s = base64.b64encode(total_bytes)
    return s.decode('utf-8')


def aes_decode(s, key=b""):
    total_bytes = base64.b64decode(s)
    nonce = total_bytes[:4]
    tempkey = SHA.new(key + nonce).digest()
    cipher = ARC4.new(tempkey)
    data_bytes = cipher.decrypt(total_bytes[4:])
    data = data_bytes.decode('utf-8')
    return data


def rc4_encode(data, key=b""):
    nonce = Random.new().read(4)
    tempkey = SHA.new(key + nonce).digest()
    cipher = ARC4.new(tempkey)
    data_bytes = data.encode('utf8')
    total_bytes = nonce + cipher.encrypt(data_bytes)
    s = base64.b64encode(total_bytes)
    return s.decode('utf-8')


def rc4_decode(s, key=b""):
    total_bytes = base64.b64decode(s)
    nonce = total_bytes[:4]
    tempkey = SHA.new(key + nonce).digest()
    cipher = ARC4.new(tempkey)
    data_bytes = cipher.decrypt(total_bytes[4:])
    data = data_bytes.decode('utf-8')
    return data
