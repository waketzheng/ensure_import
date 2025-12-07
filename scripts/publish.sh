#!/usr/bin/env bash

set -e
uv build --clear
uv publish
