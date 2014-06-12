# -*- coding: utf-8 -*-

"""
:Module: batman
:Synapsis: pcap parser for TCP/IP business
:Author: JP
"""

import sys
from impacket.ImpactDecoder import EthDecoder 
from impacket.ImpactPacket import IP, TCP
from pcapy import open_offline, open_live
from numpy import array, sum, mean, std

_ethdecoder  = EthDecoder() # Ethereal (Layer 2) decoder

_pkts = []
_win_size = 100 # number of packets in a window (constant)
_last_ts = None

def is_SYN_only(tcp_flags):
    """
    Checks whether a TCP header has only the SYN flag set.
    
    Parameters
    ----------
    tcp_flags : int
       TCP flag 

    """
    return tcp_flags & ((1 << 6) - 1) == 2

def callback(hdr, data):
    """
    Callback invoked to process each packet.

    Parameters
    ----------
    hdr : Ether
       Ethernet header
    data : string of bytes
       packet data (raw)

    """
    global _pkts
    global _last_ts

    packet = _ethdecoder.decode(data)
    l2 = packet.child()
    if isinstance(l2, IP):
        l3 = l2.child()
        if isinstance(l3, TCP):
            ts = hdr.getts()[0]*1000000 + hdr.getts()[1]
            if len(_pkts) == 0:
                _last_ts = ts
            interarrival = ts - _last_ts
            _last_ts = ts
            _pkts.append({'SYN_only':is_SYN_only(l3.get_th_flags()), \
                              "interarrival":interarrival # time interval between this pkt and the last one
                          })
            if is_SYN_only(l3.get_th_flags()) or 1:
                print 'Got TCP-SYN %s:%s -> %s:%s'%(l2.get_ip_src(), l3.get_th_sport(), l2.get_ip_address(0), l3.get_th_dport())

if __name__ == '__main__':
    # sanitize command-line
    ofh = -1
    if len(sys.argv) < 2:
        print "Usage: python %s <input_pcap_file> [output_file]"%sys.argv[0]
        sys.exit(-1)

    if len(sys.argv) > 2:
        ofh = open(sys.argv[2], 'a')

    max_bytes = 1024
    promisc = False
    read_timeout = 100
    dev = sys.argv[1]
    devil = open_live(dev, max_bytes, promisc, read_timeout)
    
    # start main loop
    devil.loop(0, callback)

    # now we have a bail of TCP packets, process them!
    for j in xrange(len(_pkts) - _win_size):
        SYN_only_ratio = 1.0*sum([pkt.get('SYN_only') for pkt in _pkts[j:j+_win_size]])/_win_size
        interarrival_mean = mean([pkt.get('interarrival') for pkt in _pkts[j:j+_win_size]])
        interarrival_std = std([pkt.get('interarrival') for pkt in _pkts[j:j+_win_size]])
        line = "0 1:%s 2:%s 3:%s"%(SYN_only_ratio, interarrival_mean, interarrival_std)
        print line
        if ofh > 0:
            ofh.write("%s\r\n"%line)

    # close files for sanity
    if ofh > 0:
        ofh.close()
            
