#!/usr/bin/python

"""
Synopsis: epylint wrapper that filters a bunch of false-positive warnings
and errors

"""
# Author: DOHMATOB Elvis Dopgima <gmdopp@gmail.com> <elvis.dohmatob@inria.fr>

import os
import sys
import re
from subprocess import Popen, STDOUT, PIPE

NOSE_NO_NAME = re.compile("No name '.+' in module 'nose(?:\..+)?'")
NUMPY_HAS_NO_MEMBER = re.compile("Module 'numpy(?:\..+)?' has no '.+' member")
NUMPY_NO_NAME = re.compile("No name '.+' in module 'numpy(?:\..+)?'")
SCIPY_HAS_NO_MEMBER = re.compile("Module 'scipy(?:\..+)?' has no '.+' member")
SCIPY_NO_NAME = re.compile("No name '.+' in module 'scipy(?:\..+)?'")
NIPY_HAS_NO_MEMBER = re.compile("Module 'nipy(?:\..+)?' has no '.+' member")
SK_ATTR_DEFINED_OUTSIDE_INIT = re.compile(
    "Attribute '.+_' defined outside __init__")
REL_IMPORT_SHOULD_BE = re.compile("Relative import '.+', should be '.+")
REDEFINING_NAME_FROM_OUTER_SCOPE = re.compile(
    "Redefining name '.+' from outer scope")
BUNCH_INSTANCE_NO_MEMBER = re.compile("Instance of 'Bunch' has no '.+' member")
MAYBE_NO_MEMBER = re.compile("maybe-no-member")
ARGUMENTS_NUMBER_DIFFERS = re.compile(
    "Arguments number differs from overridden method")
CELL_VARIABLE_DEFINED_IN_LOOP = re.compile("Cell variable .+? defined in loop")
WARNINGS_HAS_NO_MEMBER = re.compile(
    "Module 'warnings(?:\..+)?' has no '.+' member")

if __name__ == "__main__":
    basename = os.path.basename(sys.argv[1])
    for line in Popen(
        ['epylint', sys.argv[1], '--disable=C,R,I'  # filter thesew arnings
         ], stdout=PIPE, stderr=STDOUT, universal_newlines=True).stdout:
        if line.startswith("***********"):
            continue
        elif line.startswith("No config file found,"):
            continue
        elif "anomalous-backslash-in-string," in line:
            continue
        elif NUMPY_HAS_NO_MEMBER.search(line):
            continue
        elif NUMPY_NO_NAME.search(line):
            continue
        elif SCIPY_HAS_NO_MEMBER.search(line):
            continue
        elif SCIPY_NO_NAME.search(line):
            continue
        elif "Used * or ** magic" in line:
            continue
        elif "No module named" in line and "_flymake" in line:
            continue
        elif SK_ATTR_DEFINED_OUTSIDE_INIT.search(line):
            continue
        elif "Access to a protected member" in line:
            continue
        elif REL_IMPORT_SHOULD_BE.search(line):
            continue
        elif REDEFINING_NAME_FROM_OUTER_SCOPE.search(line):
            continue
        elif NIPY_HAS_NO_MEMBER.search(line):
            continue
        elif NOSE_NO_NAME.search(line):
            continue
        elif BUNCH_INSTANCE_NO_MEMBER.search(line):
            continue
        elif MAYBE_NO_MEMBER.search(line):
            continue
        elif ARGUMENTS_NUMBER_DIFFERS.search(line):
            continue
        elif "String statement has no effect" in line:
            continue
        elif "Used builtin function 'map'" in line:
            continue
        elif CELL_VARIABLE_DEFINED_IN_LOOP.search(line):
            break
        elif "list comprehension redefines " in line:
            continue
        elif WARNINGS_HAS_NO_MEMBER.search(line):
            continue
        # XXX extend by adding more handles for false-positives here
        else:
            print line,
