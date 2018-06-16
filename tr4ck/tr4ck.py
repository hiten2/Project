import os
import scapy, scapy.all # scapy.all.sniff(....)
import sys
import uuid

sys.path.append(os.path.realpath(__file__))

import tr4ckdb

class Tr4ck:
    
def print_callback(*args, **kwargs):
    print args[0].type
    print args, kwargs

if __name__ == "__main__":
    scapy.all.sniff(prn = print_callback) # testing scapy.all.sniff(....)
