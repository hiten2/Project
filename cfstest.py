"""gross testing script (sorry for the sloppy code)"""

import cfs
import os
import sys

if __name__ == "__main__":

    print "=" * 20, "cFS testing script", "=" * 20
    print "-" * 20, "cfs.longs", "-" * 20
    print
    print "cfs.longs.LONG_SIZE:", cfs.longs.LONG_SIZE
    i = sys.maxint + 1
    a = cfs.longs.ltoa(i)
    print "cfs.longs.ltoa(%s):" % str(i), [a]
    print "cfs.longs.ltopa(%s, %s):" % (str(i), str(cfs.longs.LONG_SIZE)), [cfs.longs.ltopa(i, cfs.longs.LONG_SIZE)]
    print "cfs.longs.atol(cfs.longs.ltoa(%s)):" % str(i), cfs.longs.atol(a)
    print
    print "-" * 20, "cfs.vacantinodequeue", "-" * 20
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

    del q
    
    print
    print "-" * 20, "cfs.inode", "-" * 20
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
    print i.read(), "(from API)"
    print [i.pio.func(file.read, i.inode_size)], "(on-disk)"
    print
    print "[altering inode contents and linking to adjacent inode]"
    i.next_index = 1
    i.write(data)

    del i
    
    i = cfs.inode.Inode(node, 1)
    i.prev_addr = 0
    i.write("hijklmnop")
    
    del i
    
    print
    print "-" * 20, "cfs.inodechain", "-" * 20
    print
    c = cfs.inodechain.InodeChain(lambda: -1, node, 0)
    print "c = cfs.inodechain.InodeChain(lambda: -1, %s, 0" % str(node)
    print "[reading forwards]"
    c.iterator()
    i = c.next()

    while i:
        print "c[%s] contents:" % str(i.index), i.read(), "(on-disk)"

        del i

        i = c.next()
    c.iterator()
    i = c.next()

    while c._cur:
        
        del i

        i = c.next()
    c.iterator(i)
    print "[reading backwards]"

    while i:
        print "c[%s] contents:" % str(i.index), i.read(), "(on-disk)"

        del i

        i = c.prev()
    
    del c
    
    node.close()
