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
