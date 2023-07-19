#!/bin/sh -e
set -x

TARGET="ensure_import"

ruff --fix $TARGET
black $TARGET
isort $TARGET
