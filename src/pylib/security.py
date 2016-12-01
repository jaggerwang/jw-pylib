import hmac
import urllib.parse


def password_hash(password, salt):
    return hmac.new(salt.encode(), password.encode()).hexdigest()


def sign_query(query, salt):
    """Sign query string for http request.

    The sign result is not relevant to key order in query string.

    :arg string|dict query: query string to be signed, also can be a dict
    :arg string salt: sign key, should be keeping secret
    """
    if isinstance(query, str):
        query = urllib.parse.parse_qs(query)

    query = {k: ("".join(v) if isinstance(v, list) else v)
             for k, v in query.items() if v is not None}
    query = ["{}={}".format(*v) for v in sorted(query.items())]
    query = '&'.join(query)
    return hmac.new(salt.encode(), query.encode()).hexdigest()
