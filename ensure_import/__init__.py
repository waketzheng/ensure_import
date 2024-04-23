import importlib
import importlib.metadata
import logging
import platform
import re
import shlex
import subprocess
import sys
from contextlib import AbstractContextManager
from functools import cached_property
from pathlib import Path
from typing import Dict, Final, List, Optional, Union

logger = logging.getLogger(__name__)

PathLike = Union[str, Path]
try:
    __version__ = importlib.metadata.version("ensure_import")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.1.0"

__all__ = ("__version__", "EnsureImport")


class EnsureImport(AbstractContextManager):
    """Auto install modules if import error.

    Usage::
        >>> while _ei := EnsureImport():
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
    RETRY: Final = 30
    retry = RETRY
    inited = False
    instances: Dict[str, "EnsureImport"] = {}

    @classmethod
    def reset(cls) -> None:
        cls.inited = False
        cls.instances.clear()

    def __new__(cls, *args, **kwargs):
        if (key := f"*{args}, **{kwargs}") in cls.instances:
            if kwargs.get("_debug"):
                print("云中谁寄锦书来，或恐是同乡, cache hint")
            return cls.instances[key]
        self = cls.instances[key] = super().__new__(cls)
        if kwargs.get("_debug"):
            print("千磨万击还坚韧，管它春下雨秋冬, initialed")
        return self

    def __init__(
        self,
        _sys_path: Optional[Union[PathLike, List[PathLike]]] = None,
        _workdir: Optional[PathLike] = None,
        _install: Optional[bool] = None,
        _no_venv: Optional[bool] = None,
        _exit=None,
        _debug=False,
        **kwargs,
    ) -> None:
        """
        :Param _sys_path: directory path to append to sys.path
        :Param _workdir: working directory, default to Path.cwd
        :Param _install: install by pip if module not found
        :Param _no_venv: do not use `python -m venv venv` to create virtual environment
        :Param _exit: whether call sys.exit when install error
        :Param kwargs: package name mapping,  example: doten='python-dotenv'
        """
        if self.inited:
            return
        self._success = True
        self._mapping = kwargs
        self._trying = True
        self._tried = 0
        self._py_path = sys.executable
        self.inited = True
        self._debug = _debug
        self._set_params(
            _sys_path,
            _workdir,
            _install,
            _no_venv,
            _exit,
        )
        if _debug:
            print(f"{self._tried = }; {self._trying = }")

    def _set_params(
        self,
        _sys_path=None,
        _workdir=None,
        _install=None,
        _no_venv=None,
        _exit=True,
    ) -> None:
        if isinstance(_workdir, str):
            _workdir = Path(_workdir)
        self._workdir = _workdir
        self._sys_path = _sys_path
        if _install is None:
            _install = _sys_path is None
        self._install = _install
        if _no_venv is None:
            if _install is False:
                _no_venv = True
            else:
                _no_venv = _sys_path is not None
        self._no_venv = _no_venv
        if _exit is None:
            _exit = _sys_path is None
        self._exit = _exit

    @property
    def trying(self) -> bool:
        if self._debug:
            print("jjjjjjjjjjjjjj", "trying called", f"{self._tried = }")
        if self._tried >= self.RETRY:
            self._trying = False
        else:
            self._tried += 1
        if self._debug:
            print("kkkkkkkkkkkkkkkkk", f"{self._tried = }; {self._trying = }")
        if self._trying:
            return True
        self._trying = True
        return False

    def __bool__(self) -> bool:
        if self._debug:
            print(1111111111111)
            print("__bool__", self, self._tried, self._trying)
            print(22222222222222)
        return self.trying

    def _clear_kw(self, packages) -> None:
        if packages:
            params = ("_sys_path", "_workdir", "_no_venv", "_exit", "_install")
            self._set_params(**{k: packages.pop(k, None) for k in params})

    def __call__(self, **packages) -> "EnsureImport":
        return self.auto_load(**packages)

    def auto_load(self, **packages) -> "EnsureImport":
        self._clear_kw(packages)
        return self

    @property
    def ok(self) -> bool:
        return self._success

    def extend_paths(self, p: Union[PathLike, List[PathLike]]) -> bool:
        if isinstance(p, (str, Path)):
            if isinstance(p, str):
                if (_p := Path(p)).is_file():
                    p = _p.parent.as_posix()
            else:
                if p.is_file():
                    p = p.parent
                p = p.as_posix()
            if p not in sys.path:
                sys.path.append(p)
                return True
            return False
        elif isinstance(p, (list, set, tuple)):
            return any(self.extend_paths(i) for i in p)
        else:
            raise TypeError(f"Expected: str/Path/List/Set/Tuple\nGot: {type(p)}")

    def __enter__(self, *args, **kw):
        if self._debug:
            print("0000000000000 Entering", f"{self._tried = }")
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        if self._debug:
            print(1111111111111111111, f"{self._tried = }")
        if isinstance(exc_value, ImportError):
            if self._debug:
                print(22222222222222)
            if (p := self._sys_path) is None:
                if self._debug:
                    print(
                        333, f"{self._tried<self.RETRY=};{self._tried=};{self.RETRY=}"
                    )
                if self._tried < self.RETRY:
                    self._success = False
                    self.run(exc_value)
                    return True
            else:
                if self._debug:
                    print("aaaaaaaaaaaaaaaaaaaaa", p, self._tried)
                if self._tried <= 2:
                    if not self.extend_paths(p):
                        for m in self.get_importing_modules(exc_value):
                            try:
                                importlib.import_module(m)
                            except ImportError:
                                pass
                    return True
        else:
            if self._debug:
                print("^" * 20)
            self._trying = False
            self._success = True

    def get_importing_modules(self, e):
        modules = re.findall(r"'([a-zA-Z][0-9a-zA-Z_]+)'", str(e))
        return modules

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
        return subprocess.call(shlex.split(cmd))

    @staticmethod
    def log_error(action: str) -> None:
        logger.error(f"ERROR: failed to {action}")

    @classmethod
    def is_poetry_project(cls, dirpath: Path) -> bool:
        toml_name = "pyproject.toml"
        for _ in range(3):
            if dirpath.joinpath(toml_name).exists():
                break
            dirpath = dirpath.parent
        else:
            return False
        cmd = "poetry run python -m pip --version"
        return cls.check_shell(cmd)

    @staticmethod
    def check_shell(cmd: str) -> bool:
        return subprocess.call(shlex.split(cmd), stderr=subprocess.DEVNULL) == 0

    @staticmethod
    def get_poetry_py_path() -> Path:
        cmd = "poetry env info --path"
        r = subprocess.run(cmd.split(), capture_output=True)
        return Path(r.stdout.strip().decode())

    @cached_property
    def workdir(self) -> Path:
        if self._workdir is None:
            self._workdir = Path.cwd()
        elif self._workdir.is_file():
            self._workdir = self._workdir.parent
        return self._workdir

    @staticmethod
    def is_module_installed(name: str) -> bool:
        try:
            importlib.import_module(name)
        except ImportError:
            return False
        else:
            return True

    def install_and_extend_sys_path(self, *packages) -> int:
        py: Union[str, Path] = Path(sys.executable)
        depends = " ".join(packages)
        if not self._no_venv and not self.is_venv():
            if self.is_poetry_project(self.workdir):
                p = self.get_poetry_py_path()
                py = "poetry run python"
            else:
                p = self.workdir / "venv"
                if not p.exists():
                    if self.run_and_echo(f"{py} -m venv venv"):
                        self.log_error(f"create virtual environment for {py}")
                        return 1
                if platform.platform().lower().startswith("win"):
                    py = p / "Scripts" / "python.exe"
                else:
                    py = p / "bin/python"
            if (lib := list(p.rglob("site-packages"))[0].as_posix()) not in sys.path:
                sys.path.append(lib)
                if not self.check_shell(f"{py} -c 'import ensure_import'"):
                    sys.path.append(Path(__file__).parent.parent.as_posix())
                if self.is_module_installed(packages[0]):
                    return 0
            if self._install:
                self.run_and_echo(f"{py} -m pip install --upgrade pip")
        if self._install and self.run_and_echo(f"{py} -m pip install {depends}"):
            self.log_error(f"install {depends}")
            return 2
        return 0
