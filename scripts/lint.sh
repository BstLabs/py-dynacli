#!/usr/bin/env bash

set -e
set -x

flake8 src
black src test --check --diff
isort src test --check --diff