#!/bin/sh -e
set -x

[ -f ../pyproject.toml ] && cd ..

poetry run fast lint
