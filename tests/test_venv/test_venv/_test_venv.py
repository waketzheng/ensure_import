#!/usr/bin/env python3
import os
import shutil
import sys
from contextlib import chdir
from pathlib import Path

WORK_DIR = Path(__file__).parent
TEST_DIR = WORK_DIR.parent
for _ in range(3):
    if TEST_DIR.name != "tests":
        TEST_DIR = TEST_DIR.parent
    else:
        break
sys.path.insert(0, TEST_DIR.parent.as_posix())
from ensure_import import EnsureImport


def run_test():
    assert Path.cwd() == WORK_DIR
    origin = sys.path[:]
    venv_path = WORK_DIR / "venv"
    if venv_path.exists():
        shutil.rmtree(venv_path)

    for i in range(EnsureImport.retry):
        with EnsureImport() as _m:
            import pytz as pz
            import six
            from dotenv import load_dotenv
            from tortoise.fields import Field
            from tortoise.fields.relational import (
                ForeignKeyFieldInstance as ForeignKeyField,
            )
        if _m.ok:
            break

    assert _m.ok
    print(f"{six.__file__ = }")
    timestamp = os.path.getmtime(six.__file__)
    assert Path(pz.__file__).exists()
    load_dotenv()
    assert issubclass(ForeignKeyField, Field)
    if i != 0:
        assert venv_path.exists()
    else:
        print("It happen to be all packages in system, no need to create venv.")

    EnsureImport.reset()
    for _ in range(EnsureImport.retry):
        with EnsureImport() as _m:
            import pytz as pz
            import six
            from dotenv import load_dotenv
            from tortoise.fields import Field
            from tortoise.fields.relational import (
                ForeignKeyFieldInstance as ForeignKeyField,
            )
        if _m.ok:
            break

    assert _m.ok
    assert os.path.getmtime(six.__file__) == timestamp
    load_dotenv()
    assert pz is not None
    assert issubclass(ForeignKeyField, Field)
    _teardown(venv_path)

    sys.path = origin
    EnsureImport.reset()
    while _ei := EnsureImport():
        with _ei:
            import pytz as pz
            import six
            import trio
            from dotenv import load_dotenv
            from tortoise.fields import Field
            from tortoise.fields.relational import (
                ForeignKeyFieldInstance as ForeignKeyField,
            )
    assert os.path.getmtime(six.__file__) == timestamp
    load_dotenv()
    assert pz is not None
    assert issubclass(ForeignKeyField, Field)
    print(f"{trio.__file__ = }")
    _teardown(venv_path)


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
