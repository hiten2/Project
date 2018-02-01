/* cFS */

#include <stdio.h>
#include <stdlib.h>

#ifndef CFS_H_
#define CFS_H_

/* cFS outline */
struct cFS {
  char *key;
  char *keySize;
  FILE *node;
  char *nodePath;
  long long nodeSize;
};

/* entry outline */
struct cFSEntryOLD {
  int mode; /* can be a file, directory, or a link */
  long long next; /* position of next block in the entry or -1 */
  unsigned long long pos; /* position of the entry in the node */
};

/* root outline */
struct cFSRootOLD {
  cFSEntry *entries;
  unsigned long long nEntries;
  unsigned long long size;
};

/* entry outline */
struct cFSEntry {
  char chunk[512];
};

/* BEGIN BYTE ORDER */

/* number of bytes used to represent a long long */
#undef CFS_LONG_LONG_SIZE_B
#define CFS_LONG_LONG_SIZE_B 0

/* byte where the disk size begins */
#undef CFS_SIZE_B
#define CFS_SIZE_B 1

/* then the key size */
#undef CFS_KEY_SIZE_B
#define CFS_KEY_SIZE_B(long_long_size) (CFS_SIZE_B + (long_long_size))

/* "locking" mechanism for key verification */
#undef CFS_LOCK_B
#define CFS_LOCK_B(long_long_size) (CFS_KEY_SIZE_B(long_long_size) + (long_long_size))

#undef CFS_LOCK_SIZE
#define CFS_LOCK_SIZE 1024

/* root directory mapping */
#undef CFS_ROOT_B
#define CFS_ROOT_B (CFS_LOCK_B(long_long_size) + CFS_LOCK_SIZE)

#undef CFS_ROOT_SIZE
#define CFS_ROOT_SIZE 1048576

/* body */
#undef CFS_BODY_B
#define CFS_BODY_B(long_long_size) (CFS_ROOT_B + CFS_ROOT_SIZE)
/* END BYTE ORDER */

/* header size */
#undef CFS_HEADER_SIZE
#define CFS_HEADER_SIZE(long_long_size) (CFS_ROOT_B + CFS_ROOT_SIZE)

/* minimum *usable* disk space required */
#undef CFS_MIN_STORAGE_SIZE
#define CFS_MIN_STORAGE_SIZE (4 * CFS_HEADER_SIZE)

/* get cFS long long size */
int cfs_get_long_long_size(struct cFS *cfs);

/* get cFS node size */
int cfs_get_size(struct cFS *cfs);

/* resolve cFS path to a byte position */
long long cfs_resolve_path(struct cFS *cfs, char *path);

/* deletion */
void del_cfs(struct cFS *cfs);

/* initialization */
struct cFS *init_cfs(char *nodePath, char *key, long long keySize);

#endif
