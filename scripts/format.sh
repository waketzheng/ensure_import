#!/bin/sh -e
set -x

TARGET="ensure_import"
[ -f ../pyproject.toml ] && cd ..

ruff --fix $TARGET
black $TARGET
isort $TARGET
