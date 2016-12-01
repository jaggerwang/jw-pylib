# -*- coding: utf-8 -*-

import hashlib
import base64
import json
import requests


class ZToBasic:
    ORDER_UTF8_URL = 'http://japi.zto.cn/zto/api_utf8/commonOrder'

    def __init__(self, company_id, partner_id):
        self.company_id = company_id
        self.partner_id = partner_id

    def get_data_digest(self, data):
        md5 = hashlib.md5(data+self.partner_id)
        return base64.b64encode(md5.hexdigest()).decode().strip()

    def post(self, data, msg_type):
        data = json.dumps(data)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF8'
        }
        data_digest = self.get_data_digest()
        r = requests.post(
            self.ORDER_UTF8_URL,
            data={
                'data': data,
                'data_digest': data_digest,
                'msg_type': msg_type,
                'company_id': self.company_id
            },
            headers=headers
        )
        if r.status_code == 200:
            return 0, r.json()
        return 1, None

    def order_create(self, data):
        return self.post(data, 'CREATE')

    def order_update(self, data):
        return self.post(data, 'UPDATE')

    def order_search(self, data):
        return self.post(data, 'SEARCH')

    def order_searchbycode(self, data):
        return self.post(data, 'SEARCHBYCODE')

    def order_feedback_status(self, data):
        return self.post(data, 'FEEDBACK_STATUS')
