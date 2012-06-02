from g6tools.mongo import flush_mongo, connect_to_test_db
from nose.tools import make_decorator


def flush_db(func):
    def new_func(*a, **kw):
        flush_mongo()
        func(*a, **kw)
    return make_decorator(func)(new_func)


def use_tdb(func):
    def new_func(*a, **kw):
        connect_to_test_db()
        flush_mongo()
        func(*a, **kw)
        flush_mongo()
    return make_decorator(func)(new_func)
