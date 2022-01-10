#!/bin/sh -e
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort src test --force-single-line-imports
sh ./scripts/format.sh