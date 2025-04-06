help:
	@echo  "EnsureImport development makefile"
	@echo
	@echo  "Usage: make <target>"
	@echo  "Targets:"
	@echo  "    up      Updates dev/test dependencies"
	@echo  "    deps    Ensure dev/test dependencies are installed"
	@echo  "    check   Checks that build is sane"
	@echo  "    test    Runs all tests"
	@echo  "    style   Auto-formats the code"
	@echo  "    lint    Auto-formats the code and check type hints"

up:
	poetry run fast upgrade

deps:
	poetry install --all-extras

_check:
	./scripts/check.py
check: deps _build _check

_lint:
	poetry run fast lint
lint: deps _build _lint

_test:
	poetry run fast test
test: deps _test

_style:
	./scripts/format.py
style: deps _style

_build:
	poetry build --clean
build: deps _build

ci: check _build _test
