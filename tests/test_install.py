import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    from contextlib import chdir
else:
    from contextlib_chdir import chdir

import pytest

from ensure_import import EnsureImport as _EI
from tests.utils import lock_sys_path


def test_venv(mocker):
    mocker.patch("ensure_import.EnsureImport.is_venv", return_value=False)
    with chdir(workdir := Path(__file__).parent / ("test_venv/" * 2)):
        with lock_sys_path():
            sys.path.append(workdir.as_posix())
            from _test_venv import run_test

            run_test()


def test_poetry(mocker):
    mocker.patch("ensure_import.EnsureImport.is_venv", return_value=False)
    with chdir(workdir := Path(__file__).parent / "test_poetry"):
        with lock_sys_path():
            sys.path.append(workdir.as_posix())
            from _test_poetry import run_test

            run_test()


def test_set_params():
    # _exit
    _ei = _EI()
    assert _ei._exit is True
    _ei = _EI(_exit=None)
    assert _ei._exit is True
    _ei = _ei()
    assert _ei._exit is True
    _ei = _ei(_exit=None)
    assert _ei._exit is True
    # _workdir
    _ei = _ei(_workdir=".")
    assert _ei._workdir == Path(".")
    # _sys_path, _install, _no_venv
    _ei = _EI(_install=False)
    assert _ei._no_venv is True
    _ei = _EI(_sys_path="../dir")
    assert _ei._install is False
    assert _ei._no_venv is True


def test_install_failed(mocker):
    mocker.patch(
        "ensure_import.EnsureImport.install_and_extend_sys_path", return_value=0
    )
    with pytest.raises(ModuleNotFoundError):
        while _ei := _EI(_sys_path=None, _workdir=None, _no_venv=True):
            with _ei:
                import not_exist_module
    with pytest.raises(UnboundLocalError):
        not_exist_module.main()
    assert _ei._tried >= _ei.retry
    assert _ei._trying is True
    assert _ei.trying is False
