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
    """use encryption? (maybe not really necessary)"""
    def __init__(self, node, index, inode_size = inode.INODE_SIZE, n_inodes = 1, index_size = longs.LONG_SIZE):
        assert [type(a) for a in (inode_size, n_inodes, index_size)] in [3 * [int], 3 * [long]] and inode_size > 0 and n_inodes > 0 and index_size > 0, "inode_size, n_inodes, and index_size must be of type long or int and be > 0"
        assert index >= 0, "index must be >= 0"
        self.index_size = index_size
        self.head = None
        self.inode_size = inode_size
        self.n_inodes = n_inodes # number of inodes for storing the queue
        self.pio = preservedio.PreservedIO(node, index * self.inode_size)
        self.size = 0
        self.tail = None

    def clear(self, save = True):
        """clear the queue"""
        p = self.head

        while p:
            t = p
            p = p.next

            del t
        
        self.head = None
        self.size = 0
        self.tail = None

        if save:
            self.save()
    
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
            self.save()
            return index
        return

    def enqueue(self, index):
        """enqueue an index"""
        assert self.index_size * (self.size + 1) < self.n_inodes * self.inode_size, "the queue is full"
        
        if self.head == None:
            self.head = _Node(index)
            self.tail = self.head
        else:
            self.tail.next = _Node(index)
            self.tail = self.tail.next
        self.size += 1
        self.save()
    
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
        """load the queue from disk"""
        self.clear(False) # clear but DON'T overwrite the on-disk version
        raw = self.pio.func(file.read, self.n_inodes * self.inode_size)
        self.size = longs.atol(raw[:self.index_size])
        
        for i in range(self.index_size, self.size * self.index_size, self.index_size):
            self.enqueue(longs.atol(raw[i:i + self.index_size]))

        del raw

    def save(self):
        """save the queue to disk"""
        assert self.index_size * (self.size + 1) <= self.n_inodes * self.inode_size, "too many elements in the queue"
        as_list = self.__list__()
        as_list.reverse()
        as_list.insert(0, self.size) # preface with size
        raw = "".join((longs.ltopa(i, self.index_size) for i in as_list))
        
        del as_list
        
        try:
            self.pio.__enter__()
        except Exception as e:
            raise e

        try:
            self.pio._raw_func(file.write, raw)
            self.pio._raw_func(file.flush)
            
            del raw

            self.pio.__exit__()
        except Exception as e:

            del raw
            
            try:
                self.pio.__exit__()
            except Exception as ee:
                raise ee
            raise e
        
