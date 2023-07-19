#!/usr/bin/env bash

set -e
rm -rf dist
rm -rf ../dist
poetry publish --build
