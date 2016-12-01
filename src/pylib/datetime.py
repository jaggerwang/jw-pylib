from datetime import datetime, date
import re
from time import mktime
from wsgiref.handlers import format_date_time


def date_to_int(d):
    if isinstance(d, str):
        d = date(*[int(v) for v in d.split("-")])
    return d.year * 10000 + d.month * 100 + d.day


def str_to_datetime(s):
    return datetime(*[int(v) for v in re.split(r"[- :]", s)])


def datetime_to_http_gmt(d=None):
    d = d or datetime.now()
    return format_date_time(mktime(d.timetuple()))
