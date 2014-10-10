#!/bin/bash

ALWAYS_IGNORE=E221,E701,E202,E123
OVER_INDENTED=E126,E128  # silly errors (false +ves) about indentation

epylint.py "$1" 2>/dev/null
pyflakes "$1"
pep8 --ignore=${ALWAYS_IGNORE},${OVER_INDENTED} --repeat "$1"
true
