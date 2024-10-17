#!/bin/sh -e
set -x

[ -f pyproject.toml ] || ([ -f ../pyproject.toml ] && cd ..)

poetry run ruff check --extend-select=I,B,SIM --fix .
poetry run ruff format .
