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
    node = open("dummynode.txt", "w+")
    q = cfs.vacantinodequeue.VacantInodeQueue(node, 0)
    print "q = cfs.vacantinodequeue.VacantInodeQueue(%s, 0)" % str(node)
    node.seek(0, os.SEEK_SET)
    print "q contents:", q.__list__(), "(in-memory) &", [node.read()], "(on-disk)"

    for i in range(10):
        print "q.enqueue(%s)" % str(i), "size:", q.size
        q.enqueue(i)
    node.seek(0, os.SEEK_SET)
    print "q contents:", q.__list__(), "(in-memory) &", [node.read()], "(on-disk)"

    for i in range(10):
        print "%sth q.dequeue():" % str(i), q.dequeue(), "size:", q.size
    print "q.dequeue() when empty:", str(q.dequeue())
    node.close()
