import time
from functools import wraps
from contextlib import contextmanager
import logging

logger = logging.getLogger("profile")
log_level = logging.DEBUG
log_threshhold = None


def time_func(log_level=log_level, log_threshhold=log_threshhold,
              logger=logger):
    def _time_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            r = func(*args, **kwargs)
            duration = int((time.perf_counter() - start) * 1000)
            if log_threshhold is None or duration >= log_threshhold:
                logger.log(log_level, 'time func: {}.{} {}ms'.format(
                    func.__module__, func.__name__, duration))
            return r
        return wrapper
    return _time_func


@contextmanager
def time_block(label, log_level=log_level, log_threshhold=log_threshhold,
               logger=logger):
    start = time.perf_counter()
    try:
        yield
    finally:
        duration = int((time.perf_counter() - start) * 1000)
        if log_threshhold is None or duration >= log_threshhold:
            logger.log(log_level, 'time block: {} {}ms'.format(
                label, duration))
