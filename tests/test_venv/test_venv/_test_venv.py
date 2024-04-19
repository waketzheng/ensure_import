#!/usr/bin/env python3
import os
import shutil
import sys
from contextlib import contextmanager
from pathlib import Path

if sys.version_info >= (3, 11):
    from contextlib import chdir
else:
    from contextlib_chdir import chdir

WORK_DIR = Path(__file__).parent
ROOT = WORK_DIR.parent.parent.parent.parent
sys.path.insert(0, ROOT.as_posix())
from ensure_import import EnsureImport


@contextmanager
def lock_sys_path():
    origin = sys.path[:]
    try:
        yield
    finally:
        sys.path = origin


@contextmanager
def sandbox(name="venv"):
    venv_path = WORK_DIR / name
    if venv_path.exists():
        shutil.rmtree(venv_path)
    try:
        yield venv_path
    finally:
        _teardown(venv_path)
        EnsureImport.reset()


def _a(venv_path):
    for i in range(EnsureImport.retry):
        with EnsureImport() as _m:
            import pytz as pz
            import ujson, zipp  # isort:skip
            from dotenv import load_dotenv
            from tortoise.fields import Field
            from tortoise.fields.relational import (
                ForeignKeyFieldInstance as ForeignKeyField,
            )
        if _m.ok:
            break
    assert _m.ok
    print(f"{ujson.__file__ = }")
    assert os.path.getmtime(pz.__file__)
    assert os.path.getmtime(zipp.__file__)
    load_dotenv()
    assert issubclass(ForeignKeyField, Field)
    if i != 0:
        assert venv_path.exists()
    else:
        print("It happen to be all packages in system, no need to create venv.")
    EnsureImport.reset()
    return os.path.getmtime(ujson.__file__)


def _b(venv_path, timestamp):
    for _ in range(EnsureImport.retry):
        with EnsureImport() as _m:
            import pytz as pz
            import ujson
            from dotenv import load_dotenv
            from tortoise.fields import Field
            from tortoise.fields.relational import (
                ForeignKeyFieldInstance as ForeignKeyField,
            )
        if _m.ok:
            break

    assert _m.ok
    assert os.path.getmtime(ujson.__file__) == timestamp
    load_dotenv()
    assert pz is not None
    assert issubclass(ForeignKeyField, Field)


def _c(venv_path):
    while _ei := EnsureImport():
        with _ei:
            import pytz as pz
            import trio
            import ujson
            from dotenv import load_dotenv
            from tortoise.fields import Field
            from tortoise.fields.relational import (
                ForeignKeyFieldInstance as ForeignKeyField,
            )
    assert ujson is not None
    load_dotenv()
    assert pz is not None
    assert issubclass(ForeignKeyField, Field)
    print(f"{trio.__file__ = }")


def run_test():
    assert Path.cwd() == WORK_DIR
    with sandbox() as venv_path:
        with lock_sys_path():
            timestamp = _a(venv_path)

        with lock_sys_path():
            _b(venv_path, timestamp)

    with sandbox() as venv_path:
        with lock_sys_path():
            _c(venv_path)


def _teardown(venv_path) -> None:
    try:
        shutil.rmtree(venv_path)
    except FileNotFoundError:
        ...


def main():
    if EnsureImport.is_venv():
        raise AssertionError("Do not run this script in a virtual environment!")
    with chdir(WORK_DIR):
        run_test()
    print("Test pass~")


if __name__ == "__main__":
    main()
