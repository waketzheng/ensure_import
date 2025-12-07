import importlib.metadata
import subprocess  # nosec
import sys

from ensure_import import __version__

if sys.version_info >= (3, 11):
    from contextlib import chdir

else:
    import contextlib
    import os

    class chdir(
        contextlib.AbstractContextManager
    ):  # Copied from source code of Python3.13
        """Non thread-safe context manager to change the current working directory."""

        def __init__(self, path) -> None:
            self.path = path
            self._old_cwd: list[str] = []

        def __enter__(self) -> None:
            self._old_cwd.append(os.getcwd())
            os.chdir(self.path)

        def __exit__(self, *excinfo) -> None:
            os.chdir(self._old_cwd.pop())


def test_version():
    assert importlib.metadata.version("ensure_import") == __version__
    r = subprocess.run(
        ["uv", "pip", "list", "-e"], capture_output=True, encoding="utf-8"
    )
    assert r.stdout.strip().splitlines()[-1].split()[1] == __version__
