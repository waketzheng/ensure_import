import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    from contextlib import chdir
else:
    from contextlib_chdir import chdir

import pytest

from ensure_import import EnsureImport as _EI
from tests.utils import TEST_DIR, lock_sys_path


def test_venv(mocker):
    mocker.patch("ensure_import.EnsureImport.is_venv", return_value=False)
    with chdir(workdir := TEST_DIR / ("test_venv/" * 2)):
        print(f"--> cd {workdir}")
        with lock_sys_path():
            sys.path.append(workdir.as_posix())
            from _test_venv import run_test

            run_test()


def test_dot_venv(mocker):
    mocker.patch("ensure_import.EnsureImport.is_venv", return_value=False)
    with chdir(workdir := TEST_DIR / "dot_venv"):
        print(f"--> cd {workdir}")
        if not Path(".venv").exists():
            py = ".".join([str(i) for i in sys.version_info][:2])
            cmd = f"pdm venv create --with-pip {py}"
            _EI.run_and_echo(cmd)
        with lock_sys_path():
            sys.path.append(workdir.as_posix())
            from _test_dot_venv import run_test

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


def test_auto_load_updates_mapping_and_keeps_params(mocker):
    _EI.reset()
    try:
        _ei = _EI(_install=False, _no_venv=True, _exit=False)
        _ei(custom_module="custom-package", _workdir=".")

        assert _ei._install is False
        assert _ei._no_venv is True
        assert _ei._exit is False
        assert _ei._workdir == Path(".")
        assert "_workdir" not in _ei._mapping
        assert _ei._mapping["custom_module"] == "custom-package"

        exec_mock = mocker.patch.object(_ei, "_exec")
        _ei.run(ModuleNotFoundError("No module named 'custom_module'"))
        exec_mock.assert_called_once_with("custom-package")
    finally:
        _EI.reset()


def test_run_ignores_non_missing_module_import_error(mocker):
    _EI.reset()
    try:
        _ei = _EI(_install=False)
        exec_mock = mocker.patch.object(_ei, "_exec")
        error = ImportError("cannot import name 'Thing' from 'pkg'")

        with pytest.raises(ImportError) as exc_info:
            _ei.run(error)

        assert exc_info.value is error
        exec_mock.assert_not_called()
    finally:
        _EI.reset()


def test_run_maps_dotted_missing_module_to_top_level_package(mocker):
    _EI.reset()
    try:
        _ei = _EI(google="google-cloud-storage")
        exec_mock = mocker.patch.object(_ei, "_exec")

        _ei.run(ModuleNotFoundError("No module named 'google.cloud'"))

        exec_mock.assert_called_once_with("google-cloud-storage")
    finally:
        _EI.reset()


def test_instance_cache_is_kwargs_order_independent():
    _EI.reset()
    try:
        assert _EI(foo="bar", baz="qux") is _EI(baz="qux", foo="bar")
    finally:
        _EI.reset()


def test_auto_load_refreshes_cached_workdir(tmp_path: Path):
    _EI.reset()
    try:
        first = tmp_path / "first"
        second = tmp_path / "second"
        first.mkdir()
        second.mkdir()
        _ei = _EI(_workdir=first)

        assert _ei.workdir == first

        _ei(_workdir=second)

        assert _ei.workdir == first
        assert _ei._workdir == second
    finally:
        _EI.reset()


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
