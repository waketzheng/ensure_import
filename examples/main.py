#!/usr/bin/env python3
from pathlib import Path

from ensure_import import EnsureImport as _EI

"""
The ensure_import with auto create virtual environment,
then install fastapi/uvicorn by pip.

Usage::

    python main.py

"""

while _ei := _EI():
    with _ei:
        import uvicorn
        from fastapi import FastAPI, Request


app = FastAPI(title=Path(__file__).parent.name)


@app.get("/")
async def root(request: Request):
    return {"dir(request)": dir(request)}


if __name__ == "__main__":
    uvicorn.run("__main__:app", reload=True)
