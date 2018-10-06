#!/bin/sh

echo "Running ${0}"
pip install -e .

#find ./app/ -name '*.pyc' -exec rm -f {} \;
#find . -name __pycache__ -type d -exec rm -fr {} \;

echo "Calling exec $*"
exec "$@"