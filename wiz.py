import unittest
import os
import sys
import re
import numpy

# RE patterns
pkt_pattern = "\(\d+?,\d+?,\d+?,\d+?,\d+?\)"
pkt_series_pattern = "\[%s(?:,%s)*?\]"%(pkt_pattern,pkt_pattern)

def get_tcp_flag_bits(tcp_synflag):
    """
    Extract 

the bits of the TCP flag
    """
    bits = dict()

    bits["SYN"] = 0
    if tcp_synflag&2:
        bits["SYN"] = 1

    return bits

def get_pkt_series_tcp_syn_feature(pkt_series):
    """
    Given a series of pkts, this function computes the proportion of pkts which have SYN flag 
    (5th bit of TCP flag) active.
    """
    return 1.0*len([pkt for pkt in pkt_series if get_tcp_flag_bits(int(pkt[2])).get("SYN")])/len(pkt_series)

def create_kmeans_problem_matrix(pkt_series_bail, outfile=None):
    """
    Given a group of pkt series, this function creates a feature matrix (rows are labelled by the series)
    usable by the K-means algorithm.
    """
    f = list()

    # normalize 
    for pkt_series in pkt_series_bail:
        features = (len(pkt_series), get_pkt_series_tcp_syn_feature(pkt_series))
        f.append(features)

    feature_matrix = numpy.matrix(f, dtype='double')

    if not outfile is None:
        numpy.savetxt(outfile, feature_matrix, fmt='%f')
 
    return numpy.matrix(f, dtype='double')
        
class MiscTest(unittest.TestCase):
    def test_tcp_synflag_bits(self):
        bits = get_tcp_flag_bits(2)
        self.assertEqual(bits.get("SYN"), 1)

        bits = get_tcp_flag_bits(18)
        self.assertEqual(bits.get("SYN"), 1)

        bits = get_tcp_flag_bits(16)
        self.assertEqual(bits.get("SYN"), 0)


if __name__ == '__main__':
    # unittest.main() # XXX uncomment to run unit-tests

    # read input file
    dump = open(sys.argv[1], "r").read()

    giant_clusters = dict()

    # scrape for all series of pkts
    all_pkt_series = list()
    source_ips = list()
    for item in re.finditer(pkt_series_pattern, dump):
        raw = item.group()[1:].rstrip("]")

        # parse this pkt series
        pkt_series = list()
        for item in re.finditer(pkt_pattern, raw):
            pkt = item.group()[1:].rstrip(")").split(",")
            source_ip = pkt[0]
            if not source_ip in source_ips:
                source_ips.append(source_ip)
            pkt_series.append(pkt)

        all_pkt_series.append(pkt_series)

    # form a 2-partition of the pkt bail as follows:
    # 2 pkts belong to the same class iff they belong to the same initial series and their source ips are identical.
        giant_clusters = dict() # keys are source ips (not repeated)
        for source_ip in source_ips:
            giant_clusters[source_ip] = list()
            for pkt_series in all_pkt_series:
                pkt_subseries = [pkt for pkt in pkt_series if pkt[0] == source_ip] # all those pkts in the given series, whose source IP is source_ip
                if pkt_subseries:
                    giant_clusters[source_ip].append(pkt_subseries)
                

    # beautiful print 
    count = 0
    for source_ip in giant_clusters.keys():
        print create_kmeans_problem_matrix(giant_clusters[source_ip], "feature_matrix_%s.dat"%source_ip)
        # for pkt_series in giant_clusters[source_ip]:
        #     # problem matrix for kmeans algo
        #     kmeans_problem_matrix = pkt_series
        #     print kmeans_problem_matrix
        count += 1


        # print boundary line
        if count < len(giant_clusters):
            print "#"*125
