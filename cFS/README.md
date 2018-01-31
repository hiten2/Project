# a basic encrypted filesystem (for now)
*for now it includes a tree mapping area, mut maybe not even have directory trees, just files?*
*I'm going to proceed under the assumption that there could be a tree structure, and will clarify resource access methods in the API*

## general outline
### byte order
*let MKRHOST be the host that ran `mkfs.cfs`*
**header:**
byte 0: (length = 1 byte) size of `long long`
bytes 1 (length = size of `long long` on MKRHOST): disk size
bytes (variable start) (length = size of `long long` on MKRHOST): key size
bytes (variable start) (length = 1024): "locking" mechanism (used for key validation)
bytes (variable start) (length = 1048576): tree structure mapping (for root directory)
bytes (variable start) (length -> end): content
