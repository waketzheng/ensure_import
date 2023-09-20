#!/usr/bin/env python3
from pathlib import Path

from ensure_import import EnsureImport as _EI

while _ei := _EI():
    with _ei:
        import uvicorn
        from fastapi import FastAPI, Request


app = FastAPI(title=Path(__file__).parent.name)


@app.get("/")
async def root(request: Request):
    return {"dir(request)": dir(request)}


if __name__ == "__main__":
    uvicorn.run(f"{Path(__file__).stem}:app")
