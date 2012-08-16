# -*- coding: utf-8 -*-

"""
:Module: formats
:Synopsis: Module exporting basic functions for converting data files between different (text) formats (e.g LIBSVM format, etc.)
:Author: JP
"""

import sys
import re

def convert_from_libsvm_format(infile, outfile=None):
    """
    Converts from LIBSVM data format to 'more' standard format loadable by R, numpy, etc.
    
    Parameters
    ----------
    infile : string
       libsvm input data filename
       outfile : string, optional (default None)
       output filename

    Examples
    --------
    >>> 1 + 1 
    2

    """
    ofh = -1
    if not outfile is None:
        ofh = open(outfile, 'a')

    with open(infile, 'r') as ifh:
        while True:
            line = ifh.readline()
            if not line:
                break
            standard_line = re.sub(" \d+?\:", " ", line)
            print standard_line
            if ofh > 0:
                ofh.write(standard_line)

    # close open files
    ifh.close()
    if ofh > 0:
        ofh.close()

if __name__ == '__main__':
    outfile = None
    if len(sys.argv) < 2:
        print "Usage: python %s <libsvm_datafile> [output_file]"%sys.argv[0]
        sys.exit(-1)
    if len(sys.argv) > 2:
        outfile = sys.argv[2]

    convert_from_libsvm_format(sys.argv[1], outfile=outfile)
