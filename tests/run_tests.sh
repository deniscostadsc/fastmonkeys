#!/bin/bash

set -e

cd $(dirname $0) && cd ..

flake8 . --ignore=F403 --max-line-length=119

py.test --cov fastmonkeys tests/
