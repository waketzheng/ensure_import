#!/usr/bin/env python3
from pathlib import Path

from ensure_import import EnsureImport


for _ in range(EnsureImport.retry):
    with EnsureImport() as _m:
        import uvicorn
        from fastapi import FastAPI
    if _m.ok:
        break


app = FastAPI(title=Path(__file__).parent.name)


if __name__ == '__main__':
    uvicorn.run('main:app')
