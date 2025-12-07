import sys
from contextlib import contextmanager
from pathlib import Path

TEST_DIR = Path(__file__).parent


@contextmanager
def lock_sys_path():
    origin = sys.path[:]
    try:
        yield
    finally:
        sys.path = origin
