/* cFS API */

#include "cfsapi.h"

/* create file *//* not done */
int cfs_create_file(struct cFS *cfs, char *path) {
  if (cfs != NULL && cfs->node != NULL && path != NULL) {
    /* pass */
    return 1;
  }
  return 0;
}

/* destroy cFS *//* not done */
int cfs_destroy(struct cFS *cfs);

/* make cFS at the given path *//* not done */
int cfs_make(struct cFS *cfs) {
  FILE *node;
  unsigned long size;
  
  if ((node = fopen(nodePath, "wb")) != NULL && (size = get_fsize(node)) > CFS_MIN_STORAGE_SIZE) {
    write((char) sizeof(long long), 1, node); /* byte 1 = size of size block */
    write(size, sizeof(long long), 1, node); /*bytes 2-size of size block = size of storage medium */
    write(key_size, 1, sizeof(long long), node);
    int i;
    
    for (i = 0; i < CFS_LOCK_SIZE; write(i++ % 512, 1, 1, node));
    
    for (i = 0; i < CFS_TREEMAP_SIZE; write('\0', 1, 1, node), i++); /* initialize tree mapping portion */
  }
}

/* read bytes from file *//* not done */
int cfs_read(struct cFS *cfs, char *buffer, char *path, int lim);

/* remove file *//* not done */
int cfs_remove_file(struct cFS *cfs, char *path);

/* shred & remove file *//* not done */
int cfs_sremove_file(struct cFS *cfs, char *path);

/* write bytes to file *//* not done */
int cfs_write(struct cFS *cfs, char *path, char *buffer, int lim);

void main(int argc, char *argv[]);
