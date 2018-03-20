from base64 import b64encode, b64decode
from urllib.parse import quote

import requests

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


class AlipayAPI(object):

    GATEWAY_URL = "https://mapi.alipay.com/gateway.do"

    def __init__(self, private_key=None, alipay_public_key=None):
        self.private_key = private_key
        self.alipay_public_key = alipay_public_key

    def sign(self, params):
        key = PKCS1_v1_5.new(RSA.importKey(self.private_key))
        s = self.params_string(params)
        sign = b64encode(key.sign(SHA.new(s.encode()))).decode()
        sign_type = "RSA"
        params.update({
            'sign': sign,
            'sign_type': sign_type,
            's': "{}&sign=\"{}\"&sign_type=\"{}\"".format(
                s, quote(sign), sign_type)
        })
        return params

    def verify(self, params):
        sign, sign_type = (b64decode(params.pop('sign')),
                           params.pop('sign_type').upper())
        if sign_type != "RSA":
            return False
        key = PKCS1_v1_5.new(RSA.importKey(self.alipay_public_key))
        if not key.verify(
                SHA.new(self.params_string(params).encode()), sign):
            return False

        if not self.verify_notify(
                params['notify_id'], params['seller_id']):
            return False

        return True

    def verify_notify(self, notify_id, partner):
        params = {
            'service': "notify_verify",
            'partner': partner,
            'notify_id': notify_id
        }
        try:
            r = requests.get(self.GATEWAY_URL, params=params, timeout=10)
        except Exception:
            return False
        return True if r.status_code == 200 and r.text == "true" else False

    def params_string(self, params):
        return '&'.join(sorted(["{}=\"{}\"".format(k, quote(str(v)))
                                for k, v in params.items() if v != ""]))
