"""inode vacancy queue interface"""

__package__ = "cfs"

import inode
import longs
import preservedio

class _Node:
    def __init__(self, data, next = None):
        self.data = data
        self.next = next

class VacantInodeQueue:
    """API for managing a queue of vacant inodes on primary and secondary storage"""
    def __init__(self, node, index, size = inode.INODE_SIZE, addr_size = longs.LONG_SIZE):
        self.addr_size = addr_size
        self.head = None
        self.pio = preservedio.PreservedIO(node, index * size)
        self.size = 0
        self.tail = None

    def dequeue(self):
        """dequeue an index"""
        if self.size > 0:
            index = self.head.data
            temp = self.head
            self.head = self.head.next

            del temp
            
            self.size -= 1

            if not self.size:
                self.tail = None
            self.flush()
            return index
        return

    def enqueue(self, index):
        """enqueue an index"""
        if self.head == None:
            self.head = _Node(index)
            self.tail = self.head
        else:
            self.tail.next = _Node(index)
            self.tail = self.tail.next
        self.size += 1
        self.flush()

    def flush(self):
        """flush the queue to disk"""
        as_list = self.__list__()
        as_list.insert(0, self.size) # preface with size

        try:
            self.pio.__enter__()
        except Exception as e:
            raise e

        try:
            self.pio._raw_func(file.write, longs.ltopa(self.size, self.addr_size))
            self.pio.func(file.write, "".join((longs.ltopa(i, self.addr_size) for i in as_list)))
            self.pio.__exit__()
        except Exception as e:
            try:
                self.pio.__exit__()
            except Exception as ee:
                raise ee
            raise e
        self.pio.f.flush()
    
    def __len__(self):
        return self.size

    def __list__(self):
        as_list = []
        p = self.head
        
        while p:
            as_list.append(p.data)
            p = p.next
        return as_list

    def load(self):
        """load from disk"""
        """unfinished; needs to load size as well"""
        pass
