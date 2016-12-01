import base64

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


class PingppAPI(object):

    def __init__(self, app_id, app_key, pingpp_pub_key):
        self.app_id = app_id
        self.app_key = app_key
        self.pingpp_pub_key = pingpp_pub_key

    def verify(self, sign, data):
        pkcs = PKCS1_v1_5.new(RSA.importKey(self.pingpp_pub_key))
        return pkcs.verify(SHA256.new(data), self.decode_base64(sign.encode()))

    def decode_base64(self, data):
        missing_padding = 4 - len(data) % 4
        if missing_padding:
            data += b'=' * missing_padding
        return base64.decodebytes(data)
