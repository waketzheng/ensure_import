# ensure_import
Auto install third part packages by pip into virtual environment when import error.

## Install
```bash
pip install ensure_import
```

## Usage
- Simple case that package name is module name
```py
from ensure_import import EnsureImport

for _ in range(EnsureImport.retry):
    with EnsureImport() as _m:
        import uvicorn
        from fastapi import FastAPI
    if _m.ok:
        break
```
- Package name is difference from module name
```py
for _ in range(EnsureImport.retry):
    with EnsureImport(dotenv='python-dotenv', odbc='pyodbc') as _m:
        import numpy as np
        import uvicorn
        import odbc  # who's package name is `pyodbc`
        from fastapi import FastAPI
        # package name of dotenv is `python-dotenv`
        from dotenv import load_dotenv
    if _m.ok:
        break
```
