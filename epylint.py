#!/usr/bin/python

import sys
from subprocess import Popen, PIPE, STDOUT
import os
import re
from pylint import lint as lint_mod

NUMPY_IGNORE = re.compile("Module 'numpy(?:\..+)?' has no '.+' member")
SCIPY_IGNORE = re.compile("Module 'scipy(?:\..+)?' has no '.+' member")


def _get_env():
    '''Extracts the environment PYTHONPATH and appends the current sys.path to
    those.'''
    env = dict(os.environ)
    env['PYTHONPATH'] = os.pathsep.join(sys.path)
    return env

filename = sys.argv[1]
full_path = os.path.abspath(filename)
parent_path = os.path.dirname(full_path)
child_path = os.path.basename(full_path)
options = None

while parent_path != "/" and os.path.exists(os.path.join(
        parent_path, '__init__.py')):
    child_path = os.path.join(os.path.basename(parent_path), child_path)
    parent_path = os.path.dirname(parent_path)

lint_path = lint_mod.__file__
options = options or ['--disable=C,R,I']
cmd = [sys.executable, lint_path] + options + [
    '--msg-template',
    ('{path}:{line}: {category} ({msg_id}, '
     '{symbol}, {obj}) {msg}'), '-r', 'n', child_path]
process = Popen(cmd, stdout=PIPE, cwd=parent_path, stderr=STDOUT,
                env=_get_env(), universal_newlines=True)

for line in process.stdout:
    if line.startswith("No config file found"):
        continue

    if line.startswith("**********"):
        continue

    # numpy / scipy warnings (irrelevant!)
    if NUMPY_IGNORE.search(line):
        continue
    if SCIPY_IGNORE.search(line):
        continue

    print line,
