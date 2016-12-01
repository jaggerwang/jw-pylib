import logging

from redis import StrictRedis


class RedisHandler(logging.Handler):

    def __init__(self, conn_params, key, max_length=1024**3):
        super().__init__()

        self.redis_conn = StrictRedis(**conn_params)
        self.key = key
        self.max_length = max_length

    def emit(self, record):
        try:
            record = self.format(record)
            self.redis_conn.pipeline().lpush(
                self.key, record).ltrim(
                self.key, 0, self.max_length).execute()
        except Exception:
            self.handleError(record)
