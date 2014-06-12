#!/bin/bash

epylint.py "$1" 2>/dev/null
pyflakes "$1"
pep8 --ignore=E221,E701,E202 --repeat "$1"
true
