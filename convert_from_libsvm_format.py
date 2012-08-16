import sys
import re

if __name__ == '__main__':
    ofh = -1
    if len(sys.argv) < 2:
        print "Usage: python %s <libsvm_datafile> [output_file]"%sys.argv[0]
        sys.exit(-1)
    if len(sys.argv) > 2:
        ofh = open(sys.argv[2], 'a')

    with open(sys.argv[1], 'r') as ifh:
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
