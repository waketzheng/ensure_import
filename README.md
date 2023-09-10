# ensure_import
Auto install third part packages by pip into virtual environment when import error.

## Install
```bash
pip install ensure_import
```

## Usage
- Simple case that package name is module name
```py
from ensure_import import EnsureImport as _EI

while (_ei := _EI()).trying:
    with _ei:
        import uvicorn
        from fastapi import FastAPI
```
- Package name is difference from module name
```py
while (_ei := _EI()).trying:
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
while (_ei := _EI('..')).trying:
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
