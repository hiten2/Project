"""testing"""

import cfs
import sys

if __name__ == "__main__":

    print "cfs.longs\n"
    
    print "cfs.longs.LONG_SIZE:", cfs.longs.LONG_SIZE
    i = sys.maxint + 1
    a = cfs.longs.ltoa(i)
    print "cfs.longs.ltoa(%s):" % str(i), [a]
    print "cfs.longs.atol(cfs.longs.ltoa(%s)):" % str(i), cfs.longs.atol(a)

    print

    print "cfs.diskcdll"

    print "cfs.diskcdll.DiskCDLL(%s, 0, cfs.dummycipher.DummyCipher())" % node
    node = open("dummynode.txt", "r+")
    diskcdll = cfs.diskcdll.DiskCDLL(node, 0, cfs.dummycipher.DummyCipher())
    print "cfs.diskcdll._parse_cur()
    node.close()
