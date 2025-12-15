#!/usr/bin/env python3
from pathlib import Path

from ensure_import import EnsureImport

"""
The ensure_import with auto create virtual environment,
then install fastapi/uvicorn by pip.

Usage::

    python main.py

"""

with EnsureImport(modules="asynctor fastapi uvicorn"):
    from asynctor.contrib.fastapi import runserver
    from fastapi import FastAPI, Request


app = FastAPI(title=Path(__file__).parent.name)


@app.get("/")
async def root(request: Request) -> dict[str, list[str]]:
    return {"dir(request)": dir(request)}


if __name__ == "__main__":
    runserver(app)
