import os
import scapy.all
import sys

sys.path.append(os.path.realpath(__file__))

import tr4ckdb

class Tracker(tr4ckdb.Tr4ckDB):
    """base class for generalized tracking"""

    def __init__(self, directory = os.getcwd(), db_mode = "ab",
            concurrent = True, store = True, filter = lambda p: True):
        tr4ckdb.MACDB.__init__(self, directory, db_mode, concurrent, store)

        self._filter = filter

    def handle_data(self, data):
        if self._filter(data):
            id = self._generate_id(data)
            
            if self._store:
                print id, "stored to",
                self._generate_path(id, self.store(data))
            else:
                print id

    def track(self):
        """the main function"""
        raise NotImplementedError()

class PacketTracker(tr4ckdb.MACDB, Tracker):
    """
    base class for tracking packets

    capable of concurrent database manipulation and analysis
    """
    
    def __init__(self, directory = os.getcwd(), db_mode = "ab",
            concurrent = True, store = True, filter = lambda p: True):
        Tracker.__init__(self, directory, db_mode,
            concurrent, store, filter)
        tr4ckdb.MACDB.__init__(self, directory, db_mode, concurrent, store)
    
    def track(self):
        """sniff packets into the database"""
        scapy.all.sniff(prn = self.handle_data)
