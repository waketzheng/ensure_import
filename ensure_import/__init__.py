#!/usr/bin/env python3
import platform
import re
import subprocess
import sys
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Optional


class EnsureImport(AbstractContextManager):
    """Auto install modules if import error.

    Usage::
        >>> while EnsureImport.retry:
        ...     with EnsureImport(
        ...         multipart='python-multipart', dotenv='python-dotenv'
        ...     ):
        ...         import six
        ...         import multipart
        ...         import numpy as np
        ...         from dotenv import load_dotenv
        ...         # more imports ...
        ...
    """

    mapping = {
        "multipart": "python-multipart",
        "dotenv": "python-dotenv",
        "tortoise": "tortoise-orm",
        "snap7": "python-snap7",
    }
    retry = 30
    last_one = ""

    def __init__(self, **kwargs):
        self.exception = None
        self._success = True
        self.package_mapping = dict(self.mapping, **kwargs)

    @property
    def ok(self) -> bool:
        return self._success

    def __exit__(self, exc_type, exc_value, traceback):
        print("0" * 20, exc_type, exc_value, traceback)
        if exc_value is None:
            if self.retry == 1:
                self.__class__.retry = 0
            else:
                self.__class__.retry = 1
            print("=" * 20, exc_type, exc_value, traceback)
        elif isinstance(exc_value, (ImportError, ModuleNotFoundError)):
            print("+" * 20, exc_type, exc_value, traceback)
            self.exception = exc_value
            self._success = False
            return self.run()
        else:
            print("-" * 20, exc_type, exc_value, traceback)

    def run(self) -> Optional[bool]:
        e = self.exception
        modules = re.findall(r"'([a-zA-Z][0-9a-zA-Z_-]+)'", str(e))
        if not modules or "--no-install" in sys.argv:
            raise e
        if modules[-1] == self.last_one:
            print(88888888888, self.last_one)
            return False
        if mp := self.package_mapping:
            modules = [mp.get(i, i) for i in modules]
        if rc := self.install_and_extend_sys_path(*modules):
            sys.exit(rc)
        return True

    @staticmethod
    def is_venv() -> bool:
        """Whether in virtual environment(also work for poetry)"""
        if hasattr(sys, "real_prefix"):
            return True
        return hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix

    @staticmethod
    def run_and_echo(cmd: str) -> int:
        print("--> Executing shell command:\n", cmd, flush=True)
        return subprocess.call(cmd, shell=True)

    @staticmethod
    def log_error(action: str) -> None:
        print(f"ERROR: failed to {action}")

    @classmethod
    def update_state(cls, module: str) -> None:
        cls.last_one = module
        if cls.retry > 0:
            cls.retry -= 1

    @classmethod
    def install_and_extend_sys_path(cls, *packages: str) -> int:
        py = Path(sys.executable)
        depends = " ".join(packages)
        if not cls.is_venv():
            if not (p := Path("venv")).exists():
                if cls.run_and_echo(f"{py} -m venv venv"):
                    cls.log_error(f"create virtual environment for {py}")
                    return 1
            if platform.platform().lower().startswith("win"):
                py = p / "Scripts" / "python.exe"
            else:
                py = p / "bin/python"
            # cls.run_and_echo(f"{py} -m pip install --upgrade pip ensure_import")
            cls.run_and_echo(f"{py} -m pip install --upgrade pip")
            cls.run_and_echo(f"{py} -m pip install -e .")
            lib = list(p.rglob("site-packages"))[0]
            sys.path.append(lib.as_posix())
        if cls.run_and_echo(f"{py} -m pip install {depends}"):
            cls.log_error(f"install {depends}")
            return 2
        cls.update_state(packages[-1])
        return 0
