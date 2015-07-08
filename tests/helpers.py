from nose.tools import make_decorator

def not_raises(cls=Exception):
    def decorator(f):
        @make_decorator(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except cls as e:
                raise AssertionError("Exception is not expected: {}({})".format(type(e).__name__, e))

        return wrapper

    return decorator
