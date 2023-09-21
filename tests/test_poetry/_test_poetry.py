#!/usr/bin/env python3
import os
import shutil
import sys
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


def clear():
    for name in ("venv", ".venv"):
        venv_path = WORK_DIR / name
        if venv_path.exists():
            shutil.rmtree(venv_path)
    EnsureImport.reset()


def run_test():
    assert WORK_DIR == Path.cwd()
    clear()
    for _ in range(EnsureImport.retry):
        with EnsureImport() as _m:
            import pytz as pz
            import six
            import tomli, flit
            from dotenv import load_dotenv
            from tortoise.fields import Field
            from tortoise.fields.relational import (
                ForeignKeyFieldInstance as ForeignKeyField,
            )
        if _m.ok:
            break
    assert _m.ok
    timestamp = os.path.getmtime(six.__file__)
    assert Path(pz.__file__).exists()
    load_dotenv()
    assert tomli != flit
    assert issubclass(ForeignKeyField, Field)
    assert not WORK_DIR.joinpath("venv").exists()
    assert WORK_DIR.joinpath(".venv").exists()
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
    load_dotenv()
    assert pz is not None
    assert issubclass(ForeignKeyField, Field)
    assert os.path.getmtime(six.__file__) == timestamp
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
    load_dotenv()
    assert pz is not None
    assert issubclass(ForeignKeyField, Field)
    print(f"{trio.__file__ = }")
    assert os.path.getmtime(six.__file__) == timestamp
    clear()


def main():
    if EnsureImport.is_venv():
        raise AssertionError("Do not run this script in a virtual environment!")
    run_test()
    print("Test pass~")


if __name__ == "__main__":
    main()
