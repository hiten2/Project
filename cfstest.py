"""testing"""

import cfs
import os
import sys

if __name__ == "__main__":

    print "cfs.longs"
    print
    print "cfs.longs.LONG_SIZE:", cfs.longs.LONG_SIZE
    i = sys.maxint + 1
    a = cfs.longs.ltoa(i)
    print "cfs.longs.ltoa(%s):" % str(i), [a]
    print "cfs.longs.ltopa(%s, %s):" % (str(i), str(cfs.longs.LONG_SIZE)), [cfs.longs.ltopa(i, cfs.longs.LONG_SIZE)]
    print "cfs.longs.atol(cfs.longs.ltoa(%s)):" % str(i), cfs.longs.atol(a)
    print
    print "cfs.vacantinodequeue"
    print

    if not os.path.exists("dummyvacantinodequeue.txt"):
        with open("dummyvacantinodequeue.txt", "w") as f:
            f.write("")
    node = open("dummyvacantinodequeue.txt", "r+")
    q = cfs.vacantinodequeue.VacantInodeQueue(node, 0)
    print "q = cfs.vacantinodequeue.VacantInodeQueue(%s, 0)" % str(node)
    q.load()
    print "q.load()"
    node.seek(0, os.SEEK_SET)
    print "q contents:", q.__list__(), "(in-memory) &", [node.read()], "(on-disk)"
    
    for i in range(10):
        print "q.enqueue(%s)" % str(i), "size:", q.size
        q.enqueue(i)
    node.seek(0, os.SEEK_SET)
    print "q contents:", q.__list__(), "(in-memory) &", [node.read()], "(on-disk)"

    for i in range(10):
        print "q.dequeue() + #%s:" % str(i), q.dequeue(), "size:", q.size
    print "q.dequeue() when empty:", str(q.dequeue())
    node.close()
    print
    print "cfs.inode"
    print
    
    if not os.path.exists("dummyinode.txt"):
        with open("dummyinode.txt", "w") as f:
            f.write("")
    node = open("dummyinode.txt", "r+")
    i = cfs.inode.Inode(node, 0)
    print "i = cfs.inode.Inode(%s, 0)" % str(node)
    i.format()
    print "i.format()"
    print "i.size:", i.size
    data = "abcdefg"
    i.write(data)
    print "i.write(\"%s\") (%s bytes)" % (data, str(len(data)))
    print "i.size:", i.size
    node.seek(0, os.SEEK_SET)
    print "i contents:"
    print [i.read()], "(from API)"
    print [node.read()], "(on-disk)"
