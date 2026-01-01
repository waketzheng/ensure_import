#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Run `ruff format` to make style and `ruff check --fix` to remove unused imports

Usage:
    ./scripts/format.py

"""

import os
import sys

CMD = "fast lint --skip-mypy"
TOOL = ("poetry", "pdm", "uv", "")[1]
_parent = os.path.abspath(os.path.dirname(__file__))
work_dir = os.path.dirname(_parent)
if os.getcwd() != work_dir:
    os.chdir(work_dir)

cmd = (TOOL and (TOOL + " run ")) + CMD
if os.system(cmd) != 0:
    sys.exit(1)
