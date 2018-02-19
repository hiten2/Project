# cFS (a basic encrypted filesystem)
## development plan
1. ~~solidify `diskutil.py` to be able to perform disk-related operations and atol/ltoa conversions~~
2. ~~fix bugs in `longs.py` (so that tests in `../cfstest.py` are successful)~~
3. finish `diskcdll.py`, and make sure that it is able to store an encrypted doubly linked list on disk
4. determine a logical structure for a cFS object and its encryption standard, then optimize it for efficiency
5. compile using Cython into a shared object library

**note that security can be compromised by the cipher implementation**

**we should add a format operation--maybe rethink structure?**

*General layout follows inode structure (see below), although nodes are actually doubly-linked lists.*
![](tmp.png?raw=true)

# **NEW** REVISED ADT
## cFS class
### attr
cipher
header
inode tree
node
### func
change encryption (cipher and/or key)
format
make directory
make file

## InodeTree
### attr
block size
position
root node
### func
enter directory
list directories
resize inode (automatically/manually expand/contract)

## Inode
### attr
mode
### func
automatically parse chunk
automatically parse expanded
parse directory chunk
parse expanded directory
parse file chunk
parse expanded file

~~
## Header
### attr
key_size
long_size
vericode
### func
~~

~~
# **OLD** REVISED abstract data type (ADT)
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
~~
