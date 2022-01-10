#!/usr/bin/env bash

set -e
set -x

flake8 src test
black src test --check
isort src test --check-only