#!/usr/bin/env bash

set -e
set -x

checkfiles="ensure_import"
[ -f ../pyproject.toml ] && cd ..

((poetry run isort --check-only $checkfiles && poetry run black --check $checkfiles) ||
  (echo -e "\033[1m Please run './scripts/format.sh' to auto-fix style issues \033[0m" && false)) && \
poetry run ruff $checkfiles && \
poetry run mypy $checkfiles
