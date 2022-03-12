__all__ = ('wraps', 'compose', 'check_result', 'check_wrap')


from functools import wraps

from pattern_match import *


def compose(g, unpack_args=False):
    def decorator(f):
        @wraps(f)
        def composed(*args, **kwargs):
            intermediate = f(*args, **kwargs)
            return g(*intermediate) if unpack_args else g(intermediate)

        return composed

    return decorator


def check_result(res, *args):
    if not res:
        raise ValueError(*args)

    return res

def check_wrap(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return check_result(f(*args, **kwargs), f, args, kwargs)

    return wrapped
