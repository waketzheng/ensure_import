#!/bin/sh -e
set -x

TARGET="ensure_import"
[ -f ../pyproject.toml ] && cd ..

poetry run ruff --fix $TARGET
poetry run black $TARGET
poetry run isort $TARGET
