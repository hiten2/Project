import os
import scapy.all
import sys

sys.path.append(os.path.realpath(__file__))

import tr4ckdb

doc = """network traffic tracking/analysis"""

class Analyst:
    """base class for an analyst"""

    def __init__(self, db):
        self.db = db

class Tracker:
    """
    base class for generalized tracking
    
    a tracker maintains a (dummy) database of internet traffic
    """

    def __init__(self, db, filter = lambda p: True):
        assert isinstance(db, tr4ckdb.Tr4ckDB), "db must be a tr4ckdb.Tr4ckDB"
        self.db = db
        self._filter = filter

    def add(self, data):
        """add the data if the filter allows, and print output"""
        if self._filter(data):
            id = self.db._generate_id(data)
            
            if self.db._store:
                print id, "stored to",
                self.db._generate_path(id, self.db.store(data))
            else:
                print id
    
    def track(self):
        """the main function"""
        raise NotImplementedError()

class PacketTracker(tr4ckdb.MACDB, Tracker):
    """packet collection"""
    
    def __init__(self, *args, **kwargs):
        Tracker.__init__(self, *args, **kwargs)

        assert isinstance(self.db, tr4ckdb.MACDB), "db must be a tr4ckdb.MACDB"
    
    def track(self):
        """sniff packets into the database"""
        scapy.all.sniff(prn = self.add)
