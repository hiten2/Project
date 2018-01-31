# a basic encrypted filesystem (for now)
## NOTES/COMMENTARY
### directory tree proposal
*suppose only root directory contents were stored in the tree mapping; then one could have subdirectories stored in the body section, and they could be denoted using a flag of some kind*
### API
*the current API is rather simple, and has no concept of "opening" a resource; it could be extended easily, but we should make a plan as to what would be the most secure route to go by*

## general outline
I figure we need to meet a few criteria for cFS:

1. know device size
2. know section sizes (header & body)
3. be able to verify key without storing it
4. store resources

The byte order below should meet most of those critera, except for the header size, which is fixed.

### byte order
**header:**

*let MKRHOST be the host that ran `mkfs.cfs`*

byte 0: (length = 1 byte) size of `long long`

bytes 1 (length = size of `long long` on MKRHOST): disk size

bytes (variable start) (length = size of `long long` on MKRHOST): key size

bytes (variable start) (length = 1024): "locking" mechanism (used for key validation)

bytes (variable start) (length = 1048576): tree structure mapping (for root directory)

**body**

bytes (variable start) (length -> end): content
