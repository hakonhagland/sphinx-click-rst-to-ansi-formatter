#!/bin/bash

export MYPYPATH=src
mypy --namespace-packages --explicit-package-bases --strict src tests "$@"
