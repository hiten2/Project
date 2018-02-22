"""inode chain operations"""

__package__ = "cfs"

import inode

class InodeChain:
    """
    parsing and I/O for an inode chain
    where get_vacant_inode_index must be a function
    """
    """should be a way to determine size"""
    """needs a seek method"""
    def __init__(self, get_vacant_inode_index, *args, **kwargs):
        self.entry = inode.Inode(*args, **kwargs)
        self._cur = self.entry
        self.get_vacant_inode_index = get_vacant_inode_index

    def next(self):
        """return the next inode"""
        if not self._cur.next_index == UNKNOWN:
            self._cur = inode.Inode(
                self.entry.pio.node,
                self._cur.next_index,
                self.entry.addr_size,
                self.entry.inode_size
                )
            return self._cur
        return None

    def prev(self):
        """return the previous inode"""
        if not self._cur.prev_index == UNKNOWN:
            self._cur = inode.Inode(
                self.entry.pio.node,
                self._cur.prev_index,
                self.entry.addr_size,
                self.entry.inode_size
                )
            return self._cur
        return None

    def read(self, arr = None, b = -1, offset = 0):
        """read b bytes into the bytearray starting from the offset in the current inode"""
        """unfinished"""
        if arr == None:
            pass
        return arr
