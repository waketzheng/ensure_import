import shlex
import subprocess

import pytest

from ensure_import import EnsureImport as _EI


def _teardown():
    subprocess.run(shlex.split("poetry install --sync"))


def _run():
    while _ei := _EI(_install=False):
        with _ei:
            import asyncer

            assert asyncer is not None
            print(asyncer.__file__)


def test_no_install():
    with pytest.raises(ModuleNotFoundError):
        _run()
    _teardown()
