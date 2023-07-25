#!/usr/bin/env python3
from pathlib import Path

from ensure_import import EnsureImport

count = 0
print(f"{EnsureImport.retry = }, {EnsureImport.last_one=}")
while EnsureImport.retry:
    with EnsureImport():
        import uvicorn
        from fastapi import FastAPI
    print(33333333, EnsureImport.retry, EnsureImport.last_one)
    if count > 10:
        break
    count += 1
    print(f"{FastAPI = }")


app = FastAPI(title=Path(__file__).parent.name)


if __name__ == "__main__":
    uvicorn.run("main:app")
