#!/usr/bin/env bash

set -e
set -x

checkfiles="ensure_import"
[ -f ../pyproject.toml ] && cd ..

((poetry run ruff check $checkfiles && poetry run ruff format --check $checkfiles) ||
  (echo -e "\033[1m Please run './scripts/format.sh' to auto-fix style issues \033[0m" && false)) && \
poetry run mypy $checkfiles
