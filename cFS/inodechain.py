"""inode chain operations"""

__package__ = "cfs"

import inode

class InodeChain:
    """
    parsing and I/O for an inode chain
    where get_vacant_inode_index must be a function
    """
    """should be a way to determine size"""
    def __init__(self, get_vacant_inode_index, *args, **kwargs):
        self.entry = inode.Inode(*args, **kwargs)
        self._cur = self.entry
        self.get_vacant_inode_index = get_vacant_inode_index

    def next(self):
        """return the next inode"""
        self._cur = self._cur.next()
        return self._cur

    def prev(self):
        """return the previous inode"""
        self._cur = self._cur.prev()
        return self._cur

    def read(self, arr = None, b = -1, offset = 0):
        """read b bytes into the bytearray starting from the offset in the current inode"""
        """unfinished"""
        if arr == None:
            pass
        return arr
