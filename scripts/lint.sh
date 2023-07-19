#!/usr/bin/env bash

set -e
set -x

TARGET="ensure_import"
[ -f ../pyproject.toml ] && cd ..

isort --check-only $TARGET
ruff $TARGET
mypy $TARGET
black --check $TARGET
