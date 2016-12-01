import pickle
from uuid import uuid4


class RedisSessionStore:

    def __init__(self, redis, **options):
        self.options = {
            'key_prefix': 'session',
            'expires_days': None,
        }
        self.options.update(options)
        self.redis = redis

    def prefixed(self, sid):
        return "{}:{}".format(self.options['key_prefix'], sid)

    def new_sid(self):
        return uuid4().hex

    def get_session(self, sid, name):
        data = self.redis.hget(self.prefixed(sid), name)
        session = pickle.loads(data) if data else dict()
        return session

    def set_session(self, sid, name, data):
        self.redis.hset(self.prefixed(sid), name, pickle.dumps(data))
        if self.options['expires_days']:
            self.redis.expire(
                self.prefixed(sid), self.options['expires_days'] * 86400)

    def delete_session(self, sid):
        self.redis.delete(self.prefixed(sid))

    def refresh_session(self, sid):
        if self.options['expires_days']:
            self.redis.expire(
                self.prefixed(sid), self.options['expires_days'] * 86400)

    def get_sids(self):
        return [v.decode().partition(':')[2]
                for v in self.redis.keys(self.prefixed('*'))]


class Session:

    def __init__(self, session_store, sid=None):
        self._store = session_store
        self._sid = sid if sid else self._store.new_sid()
        self._data = self._store.get_session(self._sid, 'data')
        self._dirty = False

    def clear(self):
        self._store.delete_session(self._sid)
        self._data = {}
        self._dirty = False

    @property
    def store(self):
        return self._store

    @property
    def sid(self):
        return self._sid

    @property
    def data(self):
        return self._data

    def __getitem__(self, key):
        try:
            return self._data[key]
        except KeyError:
            return None

    def __setitem__(self, key, value):
        self._data[key] = value
        self._dirty = True

    def __delitem__(self, key):
        del self._data[key]
        self._dirty = True

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def __iter__(self):
        for key in self._data:
            yield key

    def __repr__(self):
        return self._data.__repr__()

    def __del__(self):
        self.save()

    def _save(self):
        self._store.set_session(self._sid, 'data', self._data)
        self._dirty = False

    def save(self, do_check=True):
        if do_check:
            if self._dirty:
                self._save()
        else:
            self._save()
