# cFS (a basic encrypted filesystem)
## development plan
1. ~~solidify `diskutil.py` to be able to perform disk-related operations and atol/ltoa conversions~~
2. fix bugs in `longs.py` (so that tests in `../cfstest.py` are successful)
3. finish `diskcdll.py`, and make sure that it is able to store an encrypted doubly linked list on disk
4. determine a logical structure for a cFS object and its encryption standard, then optimize it for efficiency
5. compile using Cython into a shared object library

**note that security can be compromised by the cipher implementation**

*General layout follows inode structure (see below), although nodes are actually doubly-linked lists.*
![](tmp.png?raw=true)

# REVISED abstract data type (ADT)
*please note that there is no concept for a link; links are represented in a cFSDirectory-formatted list*
## cFS class
*the main API*
### attributes
header
key
root directory
node
### methods
general I/O
key change

## cFSHeader class
*stores encryption and size information*
### attributes
block size
cipher
long long size
### methods
key change
key validation

## cFSDirectory class
*a cFS directory*
### attributes
block size
disk-based linked list
position
### methods
general I/O

## cFSFile class
*a cFS file*
### attributes
disk-based linked list
### methods
general I/O
