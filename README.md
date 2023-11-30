# ensure_import

[![LatestVersionInPypi](https://img.shields.io/pypi/v/ensure_import.svg?style=for-the-badge)](https://pypi.python.org/pypi/ensure_import)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge)](https://github.com/pre-commit/pre-commit)

Auto install third part packages by pip into virtual environment when import error.

## Install
```bash
pip install ensure_import
```

## Usage
- Simple case that package name is module name
```py
from ensure_import import EnsureImport as _EI

while _ei := _EI():
    with _ei:
        import uvicorn
        from fastapi import FastAPI
```
- Package name is difference from module name
```py
while _ei := _EI():
    with _ei(dotenv='python-dotenv', odbc='pyodbc'):
        import numpy as np
        import uvicorn
        import odbc  # who's package name is `pyodbc`
        from fastapi import FastAPI
        # package name of dotenv is `python-dotenv`
        from dotenv import load_dotenv
```
- Supply module path
```py
while _ei := _EI('..'):
    with _ei:
        import gunicorn
        import uvicorn
```
This is equal to:
```py
try:
    import gunicorn
    import uvicorn
except ImportError:
    import sys
    sys.path.append('..')

    import gunicorn
    import uvicorn
```
- Support `__file__`

```py
while _ei := _EI(__file__):
    with _ei:
        import local_module

# is equal to:
try:
    import local_module
except ImportError:
    import sys
    from pathlib import Path
    dirpath: str = Path(__file__).parent.as_posix()
    if dirpath not in sys.path:
        sys.path.append(dirpath)

    import local_module
```
