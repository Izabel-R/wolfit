#!/usr/bin/env bash

export WOLFIT_SETTINGS=$(pwd)/test.settings
export FLASK_ENV=test
export FLASK_DEBUG=0

coverage run --source "." --omit app/commands.py -m pytest
coverage html

if command -v xdg-open > /dev/null; then
    xdg-open htmlcov/index.html
elif command -v start > /dev/null; then
    start htmlcov/index.html
else
    echo "Coverage report available at $(pwd)/htmlcov/index.html"
fi