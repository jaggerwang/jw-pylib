import string
import random
import re


def random_string(len_=8, allowed_chars=None):
    if allowed_chars is None:
        allowed_chars = string.ascii_letters + string.digits
    return ''.join(random.sample(allowed_chars, len_))


def str_to_tags(s):
    return [v for v in re.split(r"[ ,;|]+", s)]


def display_width(s):
    """字符串显示宽度计算，英文字符宽度算1，中文字符宽度算2。

    :Parameters:
      - `s`: 字符串

    :Returns:
      - ``int``，显示宽度
    """
    pattern = u"[\u4e00-\u9fa5]+"
    searched = re.findall(pattern, s)
    ch_len = 0

    if searched:
        for x in searched:
            ch_len += len(x) * 2

    strip_ch_len = len(re.sub(pattern, u"", s))

    return ch_len + strip_ch_len


def decode_s(s, encode='utf8', is_strict=False):
    """对字符串解码
    """
    s = bytes((ord(i) for i in s if ord(i) >= 0 and ord(i) <= 256))
    errors = 'ignore'
    if is_strict:
        errors = 'strict'

    return s.decode(encode, errors=errors)
