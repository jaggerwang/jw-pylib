import requests


class MobAPI(object):

    API_DOMAIN = "https://api.sms.mob.com"

    def __init__(self, app_key, timeout=10, logger=None):
        self.app_key = app_key
        self.timeout = timeout
        self.logger = logger

    def sms_verify(self, code, phone, zone="86"):
        url = "{}/sms/verify".format(MobAPI.API_DOMAIN)
        try:
            r = requests.post(url, {
                'appkey': self.app_key,
                'code': code,
                'phone': phone,
                'zone': zone
            },  timeout=self.timeout)
        except Exception as e:
            if self.logger:
                self.logger.error("sms verify exception: {} {}".format(
                    (code, phone, zone), e))
            return 500
        return r.json().get('status', 500) if r.status_code == 200 else 500

    def sms_send(self, phone, zone="86"):
        url = "{}/sms/sendmsg".format(MobAPI.API_DOMAIN)
        try:
            r = requests.post(url, {
                'appkey': self.app_key,
                'phone': phone,
                'zone': zone
            },  timeout=self.timeout)
        except Exception as e:
            if self.logger:
                self.logger.error("sms send exception: {} {}".format(
                    (phone, zone), e))
            return 500
        return r.json().get('status', 500) if r.status_code == 200 else 500

    def sms_checkcode(self, code, phone, zone="86"):
        url = "{}/sms/checkcode".format(MobAPI.API_DOMAIN)
        try:
            r = requests.post(url, {
                'appkey': self.app_key,
                'code': code,
                'phone': phone,
                'zone': zone
            },  timeout=self.timeout)
        except Exception as e:
            if self.logger:
                self.logger.error("sms checkcode exception: {} {}".format(
                    (code, phone, zone), e))
            return 500
        return (r.json().get('status', 500) if r.status_code == 200
                else 500)
