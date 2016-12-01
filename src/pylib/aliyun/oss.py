import base64
import hmac
import hashlib
from xml.etree.ElementTree import fromstring
from mimetypes import guess_type
import urllib.parse

import requests

from ..datetime import datetime_to_http_gmt


class OSSAPI(object):

    def __init__(self, access_id, access_secret, oss_host, timeout=10):
        self.access_id = access_id
        self.access_secret = access_secret
        self.oss_host = oss_host
        self.timeout = timeout

    @staticmethod
    def sign(access_secret, method, path, headers):
        s = "{}\n".format(method)
        s = s + "{}\n".format(headers.get('Content-MD5', ""))
        s = s + "{}\n".format(headers.get('Content-Type', ""))
        s = s + "{}\n".format(headers['Date'])
        oss_headers = ["{}:{}\n".format(k.lower(), v)
                       for k, v in headers.items() if k.startswith('X-OSS-')]
        s = s + "".join(sorted(oss_headers))
        s = s + path

        h = hmac.new(access_secret.encode(), s.encode(), hashlib.sha1)
        return base64.b64encode(h.digest()).decode().strip()

    def request(self, method, path, query=None, body=None, files=None,
                headers=None, timeout=None):
        bucket, *sub_path = path.strip('/').split('/')
        url = "http://{}.{}/{}".format(bucket, self.oss_host,
                                       '/'.join(sub_path))
        headers = headers or {}
        headers['Date'] = datetime_to_http_gmt()
        headers['Authorization'] = "OSS {}:{}".format(
            self.access_id, self.sign(self.access_secret, method, path,
                                      headers))
        timeout = timeout or self.timeout
        res = requests.request(method, url, params=query, data=body,
                               files=files, headers=headers, timeout=timeout)

        if res.status_code not in [200, 204]:
            doc = fromstring(res.text)
            error = {v.tag: v.text for v in list(doc)}
            raise Exception(error)

        return res.content

    def upload_content(self, save_path, content, filename=None, mime=None,
                       headers=None, timeout=None):
        if mime is None and filename is not None:
            mime, _ = guess_type(filename)
        headers = headers or {}
        if mime is not None:
            headers['Content-Type'] = mime
        if filename is not None:
            headers['Content-Disposition'] = (
                "inline; filename*=UTF-8''{}".format(
                    urllib.parse.quote(filename.encode())))
        return self.request('PUT', save_path, body=content, headers=headers,
                            timeout=timeout)

    def upload_file(self, save_path, local_path, headers=None, timeout=None):
        *_, filename = local_path.split('/')
        with open(local_path, "rb") as f:
            return self.upload_content(save_path, f.read(), filename=filename,
                                       headers=headers, timeout=timeout)

    def delete(self, save_path, timeout=None):
        return self.request('DELETE', save_path, timeout=timeout)
