#!/bin/sh -e
set -x

[ -f ../pyproject.toml ] && cd ..

poetry run ruff check --extend-select=I --fix .
poetry run ruff format .
poetry run mypy .
