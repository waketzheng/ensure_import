#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path

WORK_DIR = Path(__file__).parent
ROOT = WORK_DIR.parent.parent.parent
sys.path.insert(0, ROOT.as_posix())
from ensure_import import EnsureImport


def clear():
    for name in ("venv", ".venv"):
        venv_path = WORK_DIR / name
        if venv_path.exists():
            shutil.rmtree(venv_path)
    EnsureImport.reset()


def _a():
    for _ in range(EnsureImport.retry):
        with EnsureImport() as _m:
            import idna
            import orjson
            import pytz as pz
            import tomli
            from dotenv import load_dotenv
            from tortoise.fields import Field
            from tortoise.fields.relational import (
                ForeignKeyFieldInstance as ForeignKeyField,
            )
        if _m.ok:
            break
    assert _m.ok
    timestamp = os.path.getmtime(orjson.__file__)
    assert pz is not None
    load_dotenv()
    assert tomli != idna
    assert issubclass(ForeignKeyField, Field)
    assert not WORK_DIR.joinpath("venv").exists()
    assert WORK_DIR.joinpath(".venv").exists() or EnsureImport.is_poetry_project(Path())
    return timestamp


def _b(timestamp):
    for _ in range(EnsureImport.retry):
        with EnsureImport() as _m:
            import orjson
            import pytz as pz
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
    assert os.path.getmtime(orjson.__file__) == timestamp


def _c(timestamp):
    while _ei := EnsureImport():
        with _ei:
            import orjson
            import pytz as pz
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
    assert os.path.getmtime(orjson.__file__) == timestamp


def run_test():
    assert WORK_DIR == Path.cwd()
    clear()
    timestamp = _a()
    EnsureImport.reset()
    _b(timestamp)
    EnsureImport.reset()
    _c(timestamp)
    clear()


def main():
    if EnsureImport.is_venv():
        raise AssertionError("Do not run this script in a virtual environment!")
    run_test()
    print("Test pass~")


if __name__ == "__main__":
    main()
