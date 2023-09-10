#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path

TEST_DIR = Path(__file__).parent
for _ in range(3):
    if TEST_DIR.name != "tests":
        TEST_DIR = TEST_DIR.parent
    else:
        break
sys.path.append(TEST_DIR.parent.as_posix())
from ensure_import import EnsureImport


def test_venv():
    venv_path = Path.cwd() / "venv"
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
    try:
        shutil.rmtree(venv_path)
    except FileNotFoundError:
        print("Do not run this in a virtual environment!")
    else:
        print("Test pass~")


def main():
    test_venv()


if __name__ == "__main__":
    main()
