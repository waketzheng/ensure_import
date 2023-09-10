import logging
import platform
import re
import subprocess
import sys
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Optional, Union

logger = logging.getLogger(__name__)


class EnsureImport(AbstractContextManager):
    """Auto install modules if import error.

    Usage::
        >>> while (_ei := EnsureImport()).trying:
        ...     with _ei(
        ...         multipart='python-multipart', dotenv='python-dotenv'
        ...     ):
        ...         import six
        ...         import multipart
        ...         import numpy as np
        ...         from anyio import Path as AioPath
        ...         from dotenv import load_dotenv
        ...         # more imports ...
        ...
    """

    mapping = {
        "multipart": "python-multipart",
        "tortoise": "tortoise-orm",
        "dotenv": "python-dotenv",
        "snap7": "python-snap7",
    }
    retry = 30
    inited = False
    instances: dict = {}

    def __new__(cls, *args, **kwargs):
        if (key := f"*{args}, **{kwargs}") in cls.instances:
            return cls.instances[key]
        obj = cls.instances[key] = super().__new__(cls)
        return obj

    def __init__(
        self, _path: Optional[Union[str, Path]] = None, _no_venv=False, _exit=True, **kwargs
    ):
        """
        :Param _path: directory path to append to sys.path
        :Param _no_venv: do not use `python -m venv venv` to create virtual environment
        :Param _exit: whether call sys.exit when install error
        :Param kwargs: package name mapping,  example: doten='python-dotenv'
        """
        if self.inited:
            return
        self._success = True
        self._exit = _exit
        if isinstance(_path, str):
            _path = Path(_path)
        self._path = _path
        self._mapping = kwargs
        self._no_venv = _no_venv
        self._trying = True
        self._tried = 0
        self._py_path = sys.executable
        self.inited = True

    @property  # Consider to use classpropoerty instead
    def trying(self) -> bool:
        if self._tried >= self.retry:
            self._trying = False
        else:
            self._tried += 1
        if self._trying:
            return True
        self._trying = True
        return False

    def _clear_kw(self, packages) -> None:
        if packages:
            for k in ("_path" "_no_venv", "_exit"):
                if (v := packages.pop(k, None)) is not None:
                    setattr(self, k, v)

    def __call__(self, **packages) -> "EnsureImport":
        return self.auto_load(**packages)

    def auto_load(self, **packages) -> "EnsureImport":
        self._clear_kw(packages)
        if self._path:
            self._extend_path(packages)
        elif self._no_venv:
            self._just_install(packages)
        else:
            self._with_venv(packages)
        return self

    def _with_venv(self, packages):
        pass

    def _just_install(self, packages):
        pass

    def _extend_path(self, packages):
        pass

    @property
    def ok(self) -> bool:
        return self._success

    def __exit__(self, exc_type, exc_value, traceback):
        if isinstance(exc_value, (ImportError, ModuleNotFoundError)):
            self._success = False
            self.run(exc_value)
            return True
        else:
            self._trying = False
            self._success = True

    def run(self, e) -> None:
        modules = re.findall(r"'([a-zA-Z][0-9a-zA-Z_]+)'", str(e))
        if not modules or "--no-install" in sys.argv:
            raise e
        package_mapping = dict(self.mapping, **self._mapping)
        ms = (package_mapping.get(i, i) for i in modules)
        rc = self.install_and_extend_sys_path(*ms)
        if rc and self._exit:
            sys.exit(rc)

    @staticmethod
    def is_venv() -> bool:
        """Whether in a virtual environment(also work for poetry)"""
        return hasattr(sys, "real_prefix") or (
            hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
        )

    @staticmethod
    def run_and_echo(cmd: str) -> int:
        logger.info(f"--> Executing shell command:\n {cmd}")
        return subprocess.call(cmd, shell=True)

    @staticmethod
    def log_error(action: str) -> None:
        logger.error(f"ERROR: failed to {action}")

    @staticmethod
    def is_poetry_project(dirpath: Path) -> bool:
        toml_name = "pyproject.toml"
        for _ in range(3):
            if dirpath.joinpath(toml_name).exists():
                break
            dirpath = dirpath.parent
        else:
            return False
        cmd = "poetry run python -m pip --version"
        return subprocess.run(cmd.split()).returncode == 0

    @staticmethod
    def get_poetry_py_path() -> Path:
        cmd = "poetry env info --path"
        r = subprocess.run(cmd.split(), capture_output=True)
        return Path(r.stdout.strip().decode())

    def testing(self) -> bool:
        d = Path.cwd()
        if d.name.startswith("test_"):
            for _ in range(3):
                d = d.parent
                if d.name == "tests" and d.parent.name == "ensure_import":
                    return True
        return False

    def install_and_extend_sys_path(self, *packages) -> int:
        py: Union[str, Path] = Path(sys.executable)
        depends = " ".join(packages)
        if not self.is_venv():
            if self._path is None:
                self._path = Path.cwd()
            elif self._path.is_file():
                self._path = self._path.parent
            if self.is_poetry_project(self._path):
                p = self.get_poetry_py_path()
                py = "poetry run python"
            else:
                p = self._path / "venv"
                if not p.exists():
                    if self.run_and_echo(f"{py} -m venv venv"):
                        self.log_error(f"create virtual environment for {py}")
                        return 1
                if platform.platform().lower().startswith("win"):
                    py = p / "Scripts" / "python.exe"
                else:
                    py = p / "bin/python"
            self.run_and_echo(f"{py} -m pip install --upgrade pip")
            if not self.testing():
                self.run_and_echo(f"{py} -m pip install ensure_import")
            if (lib := list(p.rglob("site-packages"))[0].as_posix()) not in sys.path:
                sys.path.append(lib)  # to be optimize: check exists to aviod deplicated pip i
        if self.run_and_echo(f"{py} -m pip install {depends}"):
            self.log_error(f"install {depends}")
            return 2
        return 0
