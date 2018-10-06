#!/bin/sh

echo "Running ${0}"
pip install -e .

find ./app/ -name '*.pyc' -exec rm -f {} \;

echo "Calling exec $*"
exec "$@"