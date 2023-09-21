import sys
from contextlib import chdir
from pathlib import Path

def test_venv(mocker):
    mocker.patch("ensure_import.EnsureImport.is_venv", return_value=False)
    with chdir(Path(__file__).parent / ('test_venv/' * 2)):
        sys.path.append('.')
        from _test_venv import run_test

        run_test()


def test_poetry(mocker):
    mocker.patch("ensure_import.EnsureImport.is_venv", return_value=False)
    with chdir(workdir := Path(__file__).parent / 'test_poetry'):
        sys.path.append(workdir.as_posix())
        from _test_poetry import run_test

        run_test()
