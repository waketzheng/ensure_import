#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path

TEST_DIR = Path(__file__).parent
if TEST_DIR.name != "tests":
    TEST_DIR = TEST_DIR.parent
sys.path.insert(0, TEST_DIR.parent.as_posix())
from ensure_import import EnsureImport


def test_poetry():
    if EnsureImport.is_venv():
        raise AssertionError("Do not run this script in a virtual environment!")
    venv_path = Path(__file__).parent / "venv"
    if venv_path.exists():
        shutil.rmtree(venv_path)
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
    timestamp = os.path.getmtime(six.__file__)
    assert Path(pz.__file__).exists()
    load_dotenv()
    assert issubclass(ForeignKeyField, Field)
    assert not venv_path.exists()
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


def main():
    test_poetry()
    print("Test pass~")


if __name__ == "__main__":
    main()
