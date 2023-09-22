import sys
from contextlib import contextmanager


@contextmanager
def lock_sys_path():
    origin = sys.path[:]
    try:
        yield
    finally:
        sys.path = origin
