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
	fast upgrade

deps:
	uv sync --all-extras --all-groups

_check:
	./scripts/check.py
check: deps _build _check

_lint:
	fast lint
lint: deps _build _lint

_test:
	fast test
test: deps _test

_style:
	./scripts/format.py
style: deps _style

_build:
	uv build --clear
build: deps _build

ci: check _build _test
