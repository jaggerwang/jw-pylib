import logging

import requests

logger = logging.getLogger('facepp')


class FaceppAPI(object):

    def __init__(self, api_key, api_secret, api_url):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = api_url.strip('/')

    def request(self, path, data=None, files=None):
        url = "{}{}".format(self.api_url, path)
        data = data or {}
        data.update({
            'api_key': self.api_key,
            'api_secret': self.api_secret
        })
        data = {k: v for k, v in data.items() if v is not None}

        r = requests.post(url, data=data, files=files)
        r = r.json()
        logger.debug("request facepp api: {} {} {}".format(url, data, r))

        if 'error_code' in r:
            raise FaceppException(r['error_code'], r['error'])

        return r

    def detect(self, url, mode='normal'):
        result = self.request('/detection/detect', {
            'url': url,
            'mode': mode
        })

        return result['face']

    def create_person(self, person_name, group_name=None):
        result = self.request('/person/create', {
            'person_name': person_name,
            'group_name': group_name
        })

        return result['person_id']

    def delete_person(self, person_name):
        result = self.request(
            '/person/delete', {'person_name': person_name})

        return result['success']

    def add_face_to_person(self, person_name, face_id):
        result = self.request('/person/add_face', {
            'person_name': person_name,
            'face_id': face_id
        })

        return result['success'], result['added']

    def remove_face_from_person(self, person_name, face_id):
        result = self.request('/person/remove_face', {
            'person_name': person_name,
            'face_id': face_id
        })

        return result['success'], result['removed']

    def create_group(self, group_name, person_name=None):
        result = self.request('/group/create', {
            'group_name': group_name,
            'person_name': person_name
        })

        return result['group_id']

    def delete_group(self, group_name):
        result = self.request(
            '/group/delete', {'group_name': group_name})

        return result['success']

    def add_person_to_group(self, group_name, person_name):
        result = self.request('/group/add_person', {
            'group_name': group_name,
            'person_name': person_name
        })

        return result['success'], result['added']

    def remove_person_from_group(self, group_name, person_name):
        result = self.request('/group/remove_person', {
            'group_name': group_name,
            'person_name': person_name
        })

        return result['success'], result['removed']

    def train_identify(self, group_name):
        result = self.request('/train/identify', {
            'group_name': group_name
        })

        return result['session_id']

    def recognition_identify(self, group_name, url, mode="oneface"):
        result = self.request('/recognition/identify', {
            'group_name': group_name,
            'url': url,
            'mode': mode
        })

        return result['face']

    def info_get_session(self, session_id):
        result = self.request('/info/get_session', {
            'session_id': session_id
        })

        return result


class FaceppException(Exception):
    pass
