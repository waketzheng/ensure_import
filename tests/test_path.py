import sys
from contextlib import chdir
from pathlib import Path

from ensure_import import EnsureImport as _EI


def test_path(tmp_path: Path):
    subpath = tmp_path / "module_path"
    subpath.mkdir()
    e1 = e2 = None
    with chdir(tmp_path):
        try:
            try:
                import module_name_1
            except ImportError:
                sys.path.append(subpath.name)

                import module_name_1
        except Exception as e:
            e1 = e

        try:
            while _ei := _EI(subpath.name):
                with _ei:
                    import module_name_1  # noqa: F811
        except BaseException as e:
            e2 = e

        assert e1 is not None and type(e1) is type(e2) and str(e1) == str(e2)

        m = subpath / "module_name_1.py"
        m.touch()
        while _ei := _EI(subpath.name):
            with _ei:
                import module_name_1  # noqa: F811
        assert Path(module_name_1.__file__) == m
