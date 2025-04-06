import subprocess  # nosec
import sys
from pathlib import Path

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
    r = subprocess.run(
        ["poetry", "version", "-s"], capture_output=True, encoding="utf-8"
    )
    assert r.stdout.strip().split()[-1] == __version__


def test_poetry_add(tmp_path: Path):
    package = Path(__file__).parent.resolve().parent
    with chdir(tmp_path):
        subprocess.run(["poetry", "new", "foo"])  # nosec
        with chdir("foo"):
            r = subprocess.run(["poetry", "add", package, "--lock"])  # nosec
            assert r.returncode == 0
