import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    from contextlib import chdir
else:
    from contextlib_chdir import chdir

from ensure_import import EnsureImport


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
        else:
            print(module_name_1.__file__)

        try:
            while _ei := EnsureImport(subpath):
                with _ei:
                    import module_name_1  # noqa: F811
        except BaseException as e:
            e2 = e

        assert e1 is not None and type(e1) is type(e2) and str(e1) == str(e2)
        EnsureImport.reset()

        m = subpath / "module_name_1.py"
        m.write_text("def a(): ...")
        count = 0
        print("=" * 20)
        print("subpath:", subpath, "m:", m, "text:", m.read_text())
        while _ei := EnsureImport(subpath, _debug=True):
            count += 1
            print(f"{count = }; {bool(_ei) = }; {sys.path = }")
            try:
                import module_name_1
            except Exception as e:
                print(f"{type(e) = }; {e = }", e)
            print(f'Before __enter__: {_ei._tried = }; {_ei._trying = }')
            with _ei:
                print(f"{m = }; {subpath = }; {sys.path = }")
                import module_name_1  # noqa: F811
        assert Path(module_name_1.__file__) == m
