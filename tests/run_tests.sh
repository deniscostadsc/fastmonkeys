#!/bin/bash

set -e

cd $(dirname $0) && cd ..

flake8 . --ignore=F403 --max-line-length=119

# fake secret key for tests
export SECRET_KEY='123456'

# running tests on memory
export DATABASE_URL='sqlite://'

# clean up
find . -name '.coverage' -delete
find . -name '*.pyc' -delete
rm -rf htmlcov

if [ "$1" == "--html" ]; then
    py.test --cov fastmonkeys tests/ --cov-report html
else
    py.test --cov fastmonkeys tests/ --cov-report term-missing
fi