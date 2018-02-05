"""cFS internals"""

__package__ = "cfs"

from .cfsheader import cFSHeader
import os

global ENTRY_TYPES
ENTRY_TYPES = {
    "link": 0,
    "directory": 1,
    "file": 2,
    "part": 3
    }

class cFS:
    """
    cFS format:
    to be discussed
    """
    """maybe we should have classes for each entry type, and use those to interact with this class"""
    """we should also have an on-disk doubly linked list data structure"""
    CFS_INT_SIZE = 8 # number of bytes used to store an integer on disk
    
    def __init__(self, node_path):
        assert os.path.exists(node_path), "node_path must exist"
        assert os.path.access(node_path, os.R_OK) and os.path.access(node_path, os.W_OK), "node_path must be readable and writable"
        self.node = open(node_path, "r+")
        self.node_path = node_path
    
    def create(self, path, mode = ENTRY_TYPES["file"]):
        """create a resource"""
        pass
    
    def read(self, path):
        """read a reource"""
        pass
    
    def remove(self, path):
        """remove a resource"""
        pass
    
    def sremove(self, path):
        """securely remove a resource"""
        pass
    
    def write(self, path, string = ""):
        """write a resource"""
        pass
