#!/usr/bin/env bash

set -e
uv build --clear
echo -e 'NOTE:\n  Migrated from `uv publish` to github action @2025-12. Just push a new tag to publish this library.'
