import re
import unidecode
from functools import wraps
from flask import session, redirect, url_for
from datetime import datetime
from werkzeug.contrib.cache import SimpleCache
from wtforms.validators import regexp
from pytz import UTC

is_name = regexp(
    # not using \w since it allows for unlimited underscores
    r'^[a-zA-Z0-9]+([ \-\_][a-zA-Z0-9]+)*$',
    message='Field characters can only be letters and digits with one space, \
            underscore or hyphen as separator.'
)


def slugify(timenow, str):
    """Return slug genereated from date and specified unicoded string."""
    date = datetime.date(timenow)
    unistr = unidecode.unidecode(str).lower()
    title = re.sub(r'\W+', '-', unistr).strip('-')
    return '%i/%i/%i/%s' % (date.year, date.month, date.day, title)


def utcnow():
    return datetime.utcnow().replace(tzinfo=UTC)

cache = SimpleCache()

def cached(timeout=5 * 60, key='cached/%s'):
    # ~200 req/s => ~600-800 req/s
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logged = session.get('logged_in', None)
        if not logged:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function