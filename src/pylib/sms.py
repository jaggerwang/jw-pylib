import hashlib
import xml.etree.ElementTree as ET

import requests


class SMSAPI(object):

    API_DOMAIN = "http://106.ihuyi.cn"
    CONTENT_TEMPLATE = "您的验证码是：{}。请勿泄露验证码给他人，如非本人操作则不用理会！"
    CLOUD_REWARD_TEMPLATE = "恭喜你成为了1元云购商品{}的获得者，请尽快登录应用，进入“我的云购”里领取商品。"
    NAMESPACE = {'ihuyi': 'http://106.ihuyi.cn/'}

    def __init__(self, account, password, timeout=10, logger=None):
        h = hashlib.md5(password.encode())
        self.account, self.password = account, h.hexdigest()
        self.timeout = timeout
        self.logger = logger

    def send_code(self, code, mobile, zone="86"):
        url = "{}/webservice/sms.php?method=Submit".format(SMSAPI.API_DOMAIN)
        try:
            r = requests.post(url, {
                'account': self.account,
                'password': self.password,
                'mobile': mobile,
                'content': SMSAPI.CONTENT_TEMPLATE.format(code)
            },  timeout=self.timeout)
        except Exception as e:
            if self.logger:
                self.logger.error("sms send code exception: {} {}".format(
                    (code, mobile, zone), e))
            return 500
        root = ET.fromstring(r.text)
        status = int(root.find('ihuyi:code', SMSAPI.NAMESPACE).text)
        self.logger.info("sms send code: {}".format((code, mobile, status)))
        return 200 if status == 2 else 500

    def send_cloud_reward(self, name, mobile, zone="86"):
        url = "{}/webservice/sms.php?method=Submit".format(SMSAPI.API_DOMAIN)
        try:
            r = requests.post(url, {
                'account': self.account,
                'password': self.password,
                'mobile': mobile,
                'content': SMSAPI.CLOUD_REWARD_TEMPLATE.format(name)
            },  timeout=self.timeout)
        except Exception as e:
            if self.logger:
                self.logger.error(
                    "sms send cloud reward exception: {} {}".format(
                        (name, mobile, zone), e))
            return 500
        root = ET.fromstring(r.text)
        status = int(root.find('ihuyi:code', SMSAPI.NAMESPACE).text)
        self.logger.info(
            "sms send cloud reward: {}".format((name, mobile, status)))
        return 200 if status == 2 else 500
