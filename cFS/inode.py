"""inode parsing"""

__package__ = "cfs"

import longs
import preservedio
import os

global UNKNOWN
UNKNOWN = 0 # unknown address or mode

# inode classifications

global DIRECTORY
DIRECTORY = 0

global FILE
FILE = 1

class Inode:
    """
    dull interface for inode I/O and chain traversal
    an inode can't be linked to the zeroth inode as it is reserved
    """
    def __init__(self, node, index, addr_size = longs.LONG_SIZE, size = INODE_SIZE):
        assert type(size) in (int, long) and addr_size > 0 and size > 3 * addr_size, "*size must be a positive integer > 3 * addr_size"
        self.addr_size = addr_size
        self.index = index
        self.pio = preservedio.PreservedIO(node, self.position * self.size) # wrapper for node
        self.size = size

        self.mode = UNKNOWN
        self.next_index = UNKNOWN
        self.prev_index = UNKNOWN
        
        self.read() # initializes prev/next from node

    def format(self):
        """reset the whole inode"""
        self.mode = UNKNOWN
        self.next_index = UNKNOWN
        self.prev_index = UNKNOWN

        self.write()

    def next(self):
        """return the next inode or None"""
        if not self.next_index == UNKNOWN:
            return Inode(self.pio.node, self.next_index, self.addr_size, self.size)
        return None

    def next(self):
        """return the previous inode or None"""
        if not self.prev_index == UNKNOWN:
            return Inode(self.pio.node, self.prev_index, self.addr_size, self.size)
        return None
    
    def read(self, arr = None):
        """read the inode contents into a bytearray"""
        if arr:
            assert len(arr) == self.size - (3 * self.addr-size)), "arr must be of the appropriate size"
        else:
            arr = bytearray("\x00" * self.size - (3 * self.addr-size))

        try:
            self.pio.__enter__()
        except Exception as e:
            raise e
        
        try:
            # read prev, mode, content, next
            
            self.prev_index = longs.atol(self.pio._raw_func(file.read, self.addr_size))
            self.mode = longs.atol(self.pio._raw_func(file.read, self.addr_size))
            self.pio._raw_func(file.readinto, arr)
            self.next_index = longs.atol(self.pio._raw_func(file.read, self.addr_size))
            self.pio.__exit__()
        except Exception as e:
            try:
                self.pio.__exit__()
            except Exception as ee:
                raise ee
            raise e
        return arr

    def write(self, arr = None):
        """write a bytearray into the inode"""
        if not arr:
            arr = bytearray("\x00" * self.size - (3 * self.addr_size))

        try:
            self.pio.__enter__()
        except Exception as e:
            raise e
        
        try:
            # write prev, mode, content, and next
            
            self.pio._raw_func(file.write, longs.ltopa(self.prev_index, self.addr_size))
            self.pio._raw_func(file.write, longs.ltopa(self.mode, self.addr_size))
            self.pio._raw_func(file.write, arr)
            self.pio._raw_func(file.write, longs.ltopa(self.next_index, self.addr_size))
            self.pio.__exit__()
        except Exception as e:
            try:
                self.pio.__exit__()
            except Exception as ee:
                raise ee
            raise e
