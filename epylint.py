#!/usr/bin/python

"""
Synopsis: epylint wrapper that filters a bunch of false-positive warnings and errors
Author: DOHMATOB Elvis Dopgima <gmdopp@gmail.com> <elvis.dohmatob@inria.fr>

"""

import os
import sys
import re
from subprocess import Popen, STDOUT, PIPE

NUMPY_HAS_NO_FIELD = re.compile("Module 'numpy(?:\..+)?' has no '.+' member")
SCIPY_HAS_NO_FIELD = re.compile("Module 'scipy(?:\..+)?' has no '.+' member")
SCIPY_HAS_NO_FIELD2 = re.compile("No name '.+' in module 'scipy(?:\..+)?'")
SK_ATTR_DEFINED_OUTSIDE_INIT = re.compile("Attribute '.+_' defined outside __init__")

if __name__ == "__main__":
    basename = os.path.basename(sys.argv[1])
    for line in Popen(['epylint', sys.argv[1], '--disable=C,R,I'  # filter these warnings
                       ], stdout=PIPE, stderr=STDOUT, universal_newlines=True).stdout:
        if line.startswith("***********"):
            continue
        elif line.startswith("No config file found,"):
            continue
        elif "anomalous-backslash-in-string," in line:
            continue
        if NUMPY_HAS_NO_FIELD.search(line):
            continue
        if SCIPY_HAS_NO_FIELD.search(line):
            continue
        if SCIPY_HAS_NO_FIELD2.search(line):
            continue
        if "Used * or ** magic" in line:
            continue
        if "No module named" in line and "_flymake" in line:
            continue
        if SK_ATTR_DEFINED_OUTSIDE_INIT.search(line):
            continue
        if "Access to a protected member" in line:
            continue
        # XXX extend by adding more handles for false-positives here
        else:
            print line,
