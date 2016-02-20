import os
import base64
import logging
import datetime



def random_string(length=32):
    bin_length = int(length * 3 / 4) + 1
    random_data = os.urandom(bin_length)
    encoded = base64.b64encode(random_data, altchars=b'-_')   # making random strings url-safe
    return encoded.decode()[:length]

l = logging.getLogger('logger_is')

# source: https://fightingforalostcause.net/content/misc/2006/compare-email-regex.php
EMAIL_REGEX = r'^(?!(?:(?:\x22?\x5C[\x00-\x7E]\x22?)|(?:\x22?[^\x5C\x22]\x22?)){255,})(?!(?:(?:\x22?\x5C[\x00-\x7E]' \
              r'\x22?)|(?:\x22?[^\x5C\x22]\x22?)){65,}@)(?:(?:[\x21\x23-\x27\x2A\x2B\x2D\x2F-\x39\x3D\x3F\x5E-\x7E]' \
              r'+)|(?:\x22(?:[\x01-\x08\x0B\x0C\x0E-\x1F\x21\x23-\x5B\x5D-\x7F]|(?:\x5C[\x00-\x7F]))*\x22))(?:\.(?:' \
              r'(?:[\x21\x23-\x27\x2A\x2B\x2D\x2F-\x39\x3D\x3F\x5E-\x7E]+)|(?:\x22(?:[\x01-\x08\x0B\x0C\x0E-\x1F\x21' \
              r'\x23-\x5B\x5D-\x7F]|(?:\x5C[\x00-\x7F]))*\x22)))*@(?:(?:(?!.*[^.]{64,})(?:(?:(?:xn--)?[a-z0-9]+(?:-' \
              r'[a-z0-9]+)*\.){1,126}){1,}(?:(?:[a-z][a-z0-9]*)|(?:(?:xn--)[a-z0-9]+))(?:-[a-z0-9]+)*)|(?:\[(?:(?:I' \
              r'Pv6:(?:(?:[a-f0-9]{1,4}(?::[a-f0-9]{1,4}){7})|(?:(?!(?:.*[a-f0-9][:\]]){7,})(?:[a-f0-9]{1,4}(?::[a-' \
              r'f0-9]{1,4}){0,5})?::(?:[a-f0-9]{1,4}(?::[a-f0-9]{1,4}){0,5})?)))|(?:(?:IPv6:(?:(?:[a-f0-9]{1,4}(?::' \
              r'[a-f0-9]{1,4}){5}:)|(?:(?!(?:.*[a-f0-9]:){5,})(?:[a-f0-9]{1,4}(?::[a-f0-9]{1,4}){0,3})?::(?:[a-f0-9' \
              r']{1,4}(?::[a-f0-9]{1,4}){0,3}:)?)))?(?:(?:25[0-5])|(?:2[0-4][0-9])|(?:1[0-9]{2})|(?:[1-9]?[0-9]))(?' \
              r':\.(?:(?:25[0-5])|(?:2[0-4][0-9])|(?:1[0-9]{2})|(?:[1-9]?[0-9]))){3}))\]))$'

def human_time(timestamp):
    d = datetime.datetime.fromtimestamp(timestamp)
    return d.strftime('%Y-%m-%d %H:%M:%S')

def relative_time(old):
    current = datetime.datetime.now()
    delta = current - old
    ts = delta.total_seconds()

    def minute(secs):
        return int(secs/60)
    def hour(secs):
        return int(secs/3600)
    def day(secs):
        return int(secs/86400)

    l = [
        (30, 'epp most', None),
        (60, 'fel perce', None),
        (120, 'epp egy perce', None),
        (3600, 'perce', minute),
        (86400, 'oraja', hour),
        (586400, 'napja', day),
    ]

    for limit, text, lmbd in l:
        if ts < limit:
            ret = '%s '%lmbd(ts) if lmbd else ''
            return ret + text
    return current.strftime('%B %d.')

__all__ = ['l', 'random_string', 'EMAIL_REGEX', 'human_time', 'relative_time']
