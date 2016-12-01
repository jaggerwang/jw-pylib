import hashlib
import time
import json

import requests


class UmengMessageException(Exception):
    pass


def validation_token(appkey, app_master_secret, timestamp):
    s = appkey.lower() + app_master_secret.lower() + str(timestamp)
    return hashlib.md5(s.encode()).hexdigest()


def send(appkey, app_master_secret, send_type, payload, production_mode="true",
         device_tokens=None, alias=None, alias_type=None, file_id=None,
         filter_=None, policy=None, feedback=None, description=None,
         thirdparty_id=None, timeout=10):
    timestamp = int(time.time())

    data = {
        'appkey': appkey,
        'timestamp': timestamp,
        'validation_token': validation_token(appkey, app_master_secret,
                                             timestamp),
        'payload': payload,
        'production_mode': production_mode,
        'type': send_type,
        'device_tokens': device_tokens,
        'alias': alias,
        'alias_type': alias_type,
        'file_id': file_id,
        'filter': filter_,
        'policy': policy,
        'feedback': feedback,
        'description': description,
        'thirdparty_id': thirdparty_id
    }
    data = {k: v for k, v in data.items() if v is not None}
    headers = {
        'Content-Type': "application/json"
    }
    req = requests.post("http://msg.umeng.com/api/send", data=json.dumps(data),
                        headers=headers, timeout=timeout)

    res = req.json()
    if res.get('ret') != "SUCCESS":
        raise UmengMessageException(
            round(float(res.get('data', {}).get('error_code', "1"))), res)

    return res['data']


def send_android_message(appkey, app_master_secret, send_type, custom,
                         production_mode="true", device_tokens=None,
                         alias=None, alias_type=None, file_id=None,
                         filter_=None, policy=None, feedback=None,
                         description=None, thirdparty_id=None, timeout=10):
    params = locals()
    del params['custom']

    payload = {
        'display_type': "message",
        'body': {
            'custom': custom
        }
    }

    return send(payload=payload, **params)


def send_android_notification(appkey, app_master_secret, send_type, body,
                              extra=None, production_mode="true",
                              device_tokens=None, alias=None,
                              alias_type=None, file_id=None,
                              filter_=None, policy=None, feedback=None,
                              description=None, thirdparty_id=None,
                              timeout=10):
    params = locals()
    del params['body']
    del params['extra']

    payload = {
        'display_type': "notification",
        'body': body
    }
    if extra is not None:
        payload['extra'] = extra

    return send(payload=payload, **params)


def send_ios_message(appkey, app_master_secret, send_type, alert, badge=None,
                     sound="default", content_available=None, custom=None,
                     production_mode="true", device_tokens=None, alias=None,
                     alias_type=None, file_id=None, filter_=None,
                     policy=None, feedback=None, description=None,
                     thirdparty_id=None, timeout=10):
    params = locals()
    del params['alert']
    del params['badge']
    del params['sound']
    del params['content_available']
    del params['custom']

    aps = {'alert': alert}
    if badge is not None:
        aps['badge'] = badge
    if sound is not None:
        aps['sound'] = sound
    if content_available is not None:
        aps['content-available'] = content_available
    payload = {'aps': aps}
    if custom is not None:
        payload['custom'] = custom

    return send(payload=payload, **params)


def task_status(appkey, app_master_secret, task_id, timeout=10):
    timestamp = int(time.time())

    data = {
        'appkey': appkey,
        'timestamp': timestamp,
        'validation_token': validation_token(appkey, app_master_secret,
                                             timestamp),
        'task_id': task_id
    }
    headers = {
        'Content-Type': "application/json"
    }
    req = requests.post("http://msg.umeng.com/api/status",
                        data=json.dumps(data), headers=headers,
                        timeout=timeout)

    res = req.json()
    if res['ret'] != "SUCCESS":
        raise UmengMessageException(int(res['data']['error_code']))

    return res['data']


def cancel_task(appkey, app_master_secret, task_id, timeout=10):
    timestamp = int(time.time())

    data = {
        'appkey': appkey,
        'timestamp': timestamp,
        'validation_token': validation_token(appkey, app_master_secret,
                                             timestamp),
        'task_id': task_id
    }
    headers = {
        'Content-Type': "application/json"
    }
    req = requests.post("http://msg.umeng.com/api/cancel",
                        data=json.dumps(data), headers=headers,
                        timeout=timeout)

    res = req.json()
    if res['ret'] != "SUCCESS":
        raise UmengMessageException(int(res['data']['error_code']))

    return True


def upload(appkey, app_master_secret, content, timeout=60):
    if len(content) > 5 * 1024 * 1024:
        raise UmengMessageException("content too large")

    timestamp = int(time.time())

    data = {
        'appkey': appkey,
        'timestamp': timestamp,
        'validation_token': validation_token(appkey, app_master_secret,
                                             timestamp),
        'content': content.replace("\n", "\\n")
    }
    headers = {
        'Content-Type': "application/json"
    }
    req = requests.post("http://msg.umeng.com/api/upload",
                        data=json.dumps(data), headers=headers,
                        timeout=timeout)

    res = req.json()
    if res['ret'] != "SUCCESS":
        raise UmengMessageException(int(res['data']['error_code']))

    return res['data']['file_id']
