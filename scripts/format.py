#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Run `ruff format` to make style and `ruff check --fix` to remove unused imports

Usage:
    ./scripts/format.py

"""

import os
import shlex
import subprocess
import sys


class _Tool:
    def __init__(self, name):
        # type: (str) -> None
        self.name = name

    def __str__(self):
        # type: () -> str
        return self.name


class Tools:
    poetry = _Tool("poetry")
    pdm = _Tool("pdm")
    uv = _Tool("uv")
    none = _Tool("none")


CMD = "fast lint --skip-mypy"
_tool = Tools.uv
TOOL = getattr(_tool, "name", str(_tool))
PREFIX = (
    (TOOL + " run " + "--no-sync " * (Tools.uv.name == TOOL))
    if TOOL and Tools.none.name != TOOL
    else ""
)
_parent = os.path.abspath(os.path.dirname(__file__))
work_dir = os.path.dirname(_parent)
if os.getcwd() != work_dir:
    os.chdir(work_dir)

cmd = PREFIX + CMD
if subprocess.call(shlex.split(cmd)) != 0:
    sys.exit(1)
