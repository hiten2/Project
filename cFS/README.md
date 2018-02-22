# cFS (a basic encrypted filesystem)
## development plan
1. parsers
  - ~~`cipherinterface.py`~~
  - ~~`dummycipher.py`~~
  - ~~`inode.py`~~
  - `inodechain.py`
  - (soon to be `inodetree.py`)
  - ~~`longs.py`~~
  - ~~`memshred.py`~~
  - ~~`preservedio.py`~~
  - ~~`vacantinodequeue.py`~~
2. cFS class
3. convert to Cython
4. rewrite in C

**note that security can be compromised by the cipher implementation**

**we should add a format operation--maybe rethink structure?**

*General layout follows inode structure (see below), although nodes are actually doubly-linked lists.*
![](tmp.png?raw=true)

# structure

## a cFS instance is inode-based:
- there is a header containing cryptographic information, inode vacancy queue & size constraints
- there's an entry inode (first inode of the root directory)
- within the entry inode (and subsequent directory inodes) are SHA-256/inode number (logical order) pairs (these represent containment and links)
- the inode is prefixed and suffixed by previous and next signed inode numbers
- the second item stored on an inode is its mode (file/directory)
- each inode is separately encrypted (this makes cryptanalysis more difficult and reduces block/stream-based corruption in inode chains)

## to summarize:
header: *key verification data, inode vacancy queue (for occasional wear leveling) & sizes*

inodes: *signed previous inode, mode, content, signed next inode*; **inodes are individually encrypted**

root & directory inode content: *SHA-256/signed inode pairs*

file inode content: *raw data*
