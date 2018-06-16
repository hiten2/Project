import os
import scapy, scapy.all # scapy.all.sniff(....)
import sys
import uuid

sys.path.append(os.path.realpath(__file__))

import tr4ckdb

def print_callback(*args, **kwargs):
    print args, kwargs
