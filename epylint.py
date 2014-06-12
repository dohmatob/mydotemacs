#!/usr/bin/python

import os
import sys
import re
from subprocess import Popen, STDOUT, PIPE

NUMPY_IGNORE = re.compile("Module 'numpy(?:\..+)?' has no '.+' member")
SCIPY_IGNORE = re.compile("Module 'scipy(?:\..+)?' has no '.+' member")
SCIPY_IGNORE2 = re.compile("No name '.+' in module 'scipy(?:\..+)?'")

if __name__ == "__main__":
    basename = os.path.basename(sys.argv[1])
    for line in Popen(['epylint', sys.argv[1], '--disable=C,R,I'  # filter warnings
                       ], stdout=PIPE, stderr=STDOUT, universal_newlines=True).stdout:
        if line.startswith("***********"):
            continue
        elif line.startswith("No config file found,"):
            continue
        elif "anomalous-backslash-in-string," in line:
            continue
        if NUMPY_IGNORE.search(line):
            continue
        if SCIPY_IGNORE.search(line):
            continue
        if SCIPY_IGNORE2.search(line):
            continue
        if "Used * or ** magic" in line:
            continue
        # XXX extend by adding more handles for false-positives here
        else:
            print line,
