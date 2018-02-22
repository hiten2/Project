"""inode parsing"""

__package__ = "cfs"

import cipherinterface
import dummycipher
import longs
import memshred
import preservedio
import os

global INODE_SIZE
INODE_SIZE = 512

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
    def __init__(self, node, index, addr_size = longs.LONG_SIZE, inode_size = INODE_SIZE,
            cipher = dummycipher.DummyCipher()):
        assert type(inode_size) in (int, long) and addr_size > 0 and inode_size > 3 * addr_size, "*size must be a positive integer > 3 * addr_size"
        assert isinstance(cipher, cipherinterface.CipherInterface), "cipher must be a cipherinterface.CipherInterface instance"
        self.addr_size = addr_size
        self.cipher = cipher
        self.index = index
        self.pio = preservedio.PreservedIO(node, self.index * inode_size) # wrapper for node
        self.inode_size = inode_size

        self.mode = UNKNOWN
        self.next_index = UNKNOWN
        self.prev_index = UNKNOWN
        
        self.read() # initializes node from disk

    def format(self):
        """reset the whole inode"""
        self.mode = UNKNOWN
        self.next_index = UNKNOWN
        self.prev_index = UNKNOWN

        self.write()
    
    def read(self):
        """read the inode contents"""
        arr = bytearray()
        
        try:
            # decipher

            raw = self.cipher.decipher(bytearray(self.pio.func(file.read, self.inode_size)))
            
            # unpack prev, mode, content, and next
            
            self.prev_index = longs.atol(raw[:self.addr_size])
            self.mode = longs.atol(raw[self.addr_size:2 * self.addr_size])
            arr = bytearray(raw[2 * self.addr_size:-self.addr_size])
            self.next_index = longs.atol(raw[-self.addr_size:])

            # clean

            memshred.memshred(raw)
            
            del raw
            
        except Exception as e:
            raise e
        return arr

    def write(self, arr = None):
        """write a bytearray into the inode"""
        if not arr:
            arr = bytearray("\x00" * (self.inode_size - (3 * self.addr_size)))
        
        try:
            # pack prev, mode, content, and next

            raw = bytearray("\x00" * self.inode_size)
            raw[:self.addr_size] = longs.ltopa(self.prev_index, self.addr_size)
            raw[self.addr_size:2 * self.addr_size] = longs.ltopa(self.mode, self.addr_size)
            raw[2 * self.addr_size:len(arr)] = arr
            raw[-self.addr_size:] = longs.ltopa(self.next_index, self.addr_size)

            # encipher

            raw = self.cipher.encipher(raw)
            
            # write

            self.pio.func(file.write, raw)

            # clean

            memshred.memshred(raw)

            del raw
            
        except Exception as e:
            raise e
