#!/usr/bin/python

"""
Synopsis: epylint wrapper that filters a bunch of false-positive warnings and errors
Author: DOHMATOB Elvis Dopgima <gmdopp@gmail.com> <elvis.dohmatob@inria.fr>

"""

import os
import sys
import re
from subprocess import Popen, STDOUT, PIPE

NUMPY_HAS_NO_MEMBER = re.compile("Module 'numpy(?:\..+)?' has no '.+' member")
SCIPY_HAS_NO_MEMBER = re.compile("Module 'scipy(?:\..+)?' has no '.+' member")
SCIPY_HAS_NO_MEMBER2 = re.compile("No name '.+' in module 'scipy(?:\..+)?'")
NIPY_HAS_NO_MEMBER = re.compile("Module 'nipy(?:\..+)?' has no '.+' member")
SK_ATTR_DEFINED_OUTSIDE_INIT = re.compile("Attribute '.+_' defined outside __init__")
REL_IMPORT_SHOULD_BE = re.compile("Relative import '.+', should be '.+")
REDEFINING_NAME_FROM_OUTER_SCOPE = re.compile("Redefining name '.+' from outer scope")

if __name__ == "__main__":
    basename = os.path.basename(sys.argv[1])
    for line in Popen(['epylint', sys.argv[1], '--disable=C,R,I'  # filter thesew arnings
                       ], stdout=PIPE, stderr=STDOUT, universal_newlines=True).stdout:
        if line.startswith("***********"):
            continue
        elif line.startswith("No config file found,"):
            continue
        elif "anomalous-backslash-in-string," in line:
            continue
        if NUMPY_HAS_NO_MEMBER.search(line):
            continue
        if SCIPY_HAS_NO_MEMBER.search(line):
            continue
        if SCIPY_HAS_NO_MEMBER2.search(line):
            continue
        if "Used * or ** magic" in line:
            continue
        if "No module named" in line and "_flymake" in line:
            continue
        if SK_ATTR_DEFINED_OUTSIDE_INIT.search(line):
            continue
        if "Access to a protected member" in line:
            continue
        if REL_IMPORT_SHOULD_BE.search(line):
            continue
        if REDEFINING_NAME_FROM_OUTER_SCOPE.search(line):
            continue
        if NIPY_HAS_NO_MEMBER.search(line):
            continue
        # XXX extend by adding more handles for false-positives here
        else:
            print line,
