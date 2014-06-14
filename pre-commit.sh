#!/bin/bash

echo "Entering .git/hooks/pre-commit ..."

# Run simple short tests (that don't take forever to complete :) )
epylint.py epylint.py &>commit.log

# check return code of nosetests
retcode=$?
if [ ${retcode} != "0" ]; then
    echo " Some tests failed. See commits.log for complete info. Aborting commit."
    exit $retcode
else
    echo " All tests green!"
echo "Exiting .git/hooks/pre-commit ..."
fi

exit 0  # useless but beautiful