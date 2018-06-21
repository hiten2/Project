import os
import scapy.all
import scapy.layers
import socket
import sys

sys.path.append(os.path.realpath(__file__))

import tr4ckdb

doc = """network traffic tracking/analysis"""

def filter_out_localhost(packet):
    """return False for any localhost packet"""
    if not scapy.layers.inet.IP in packet:
        return True
    localhosts = ["localhost", "localhost.localdomain", socket.gethostname()]
    packethosts = [socket.getfqdn(a)
        for a in (packet[scapy.layers.inet.IP].dst,
        packet[scapy.layers.inet.IP].src)]
    return len(set(localhosts + packethosts)) == 5

class Analyst:
    """
    base class for an analyst

    the only common factor between analysts is that a database is required
    """

    def __init__(self, db):
        assert db, "db is required"
        self.db = db

class Tracker:
    """
    base class for generalized tracking
    
    a tracker maintains a database of internet traffic
    """

    def __init__(self, db, filter = lambda p: True):
        assert isinstance(db, tr4ckdb.Tr4ckDB), "db must be a tr4ckdb.Tr4ckDB"
        self.db = db
        self._filter = filter

    def add(self, data):
        """add the data if the filter allows, and print output"""
        if self._filter(data):
            id = self.db._generate_id(data)
            
            if not id == None:
                if self.db._store:
                    print id, "stored to",
                    self.db._generate_path(id, self.db.store(data))
                else:
                    print id
    
    def track(self):
        """the main function"""
        raise NotImplementedError()

class PacketTracker(Tracker):
    """packet collection"""
    
    def __init__(self, *args, **kwargs):
        Tracker.__init__(self, *args, **kwargs)
    
    def track(self):
        """sniff packets into the database"""
        scapy.all.sniff(prn = self.add)
