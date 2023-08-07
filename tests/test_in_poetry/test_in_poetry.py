#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path

TEST_DIR = Path(__file__).parent
if TEST_DIR.name != "tests":
    TEST_DIR = TEST_DIR.parent
sys.path.append(TEST_DIR.parent.as_posix())
from ensure_import import EnsureImport


def test_venv():
    venv_path = Path(__file__).parent / "venv"
    if venv_path.exists():
        shutil.rmtree(venv_path)
    for _ in range(EnsureImport.retry):
        with EnsureImport() as _m:
            import pytz as pz
            import six
            from dotenv import load_dotenv
            from tortoise.fields import Field, ForeignKeyField
        if _m.ok:
            break
    assert _m.ok
    timestamp = os.path.getmtime(six.__file__)
    assert Path(pz.__file__).exists()
    load_dotenv()
    assert isinstance(ForeignKeyField, Field)
    assert not venv_path.exists()
    for _ in range(EnsureImport.retry):
        with EnsureImport() as _m:
            import pytz as pz
            import six
            from dotenv import load_dotenv
            from tortoise.fields import Field, ForeignKeyField
        if _m.ok:
            break
    assert _m.ok
    load_dotenv()
    assert pz is not None
    assert isinstance(ForeignKeyField, Field)
    assert os.path.getmtime(six.__file__) == timestamp


def main():
    test_venv()
    print("Test pass~")


if __name__ == "__main__":
    main()
