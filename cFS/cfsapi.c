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

/* destroy cFS */
int cfs_destroy(struct cFS *cfs) {
  if (cfs->node != NULL) {
    for (int pass = 0; pass < 4; pass++) { /* make 4 passes */
      for (int i = 0; i < cfs->size; fwrite(rand(), 1, 1, cfs->node), i++);
    }
  }
}

/* make cFS *//* not done */
int cfs_make(struct cFS *cfs) {
  if (cfs->node != NULL) {
    unsigned long long size, cur;
    cur = ftell(cfs->node);
    fseek(cfs->node, 0, SEEK_END);
    size = ftell(cfs->node);
    fseek(cfs->node, cur, SEEK_SET);
    
    if (size > CFS_MIN_STORAGE_SIZE) {
      fwrite((char) sizeof(long long), 1, cfs->node); /* sizeof(long long) */
      fwrite(size, sizeof(long long), 1, cfs->node); /* node size */
      fwrite(key_size, 1, sizeof(long long), cfs->node); /* key size */
      int i;
      
      for (i = 0; i < CFS_LOCK_SIZE; fwrite(i++ % 512, 1, 1, cfs->node)); /* "lock" */
      
      for (i = 0; i < CFS_ROOT_SIZE; fwrite('\0', 1, 1, cfs->node), i++); /* root */
    }
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

#ifndef NOAUTO

/* not done */
int main(int argc, char *argv[]) {
  char *helpString = "Usage: cfsapi <node> <op> <path> [arg]"; /* should have a key option */
  char *extHelpString = "cFS API extended help:\n" \
    "<node>\t- the containing node for the cFS\n" \
    "<op>\n" \
    "\tcreate\t- create a new file at <path>\n" \
    "\tread\t- read the file at <path>\n" \
    "\tremove\t- remove the file at <path>" \
    "\tsremove\t- shred and remove the file at <path>\n" \
    "\twrite\t- write the bytes specified by [arg] (which may be omitted)\n" \
    "<path>\t- the path to operate on" \
    "[arg]\t- the optional argument";
  char *target;
  
  
  return 0;
}

#endif
