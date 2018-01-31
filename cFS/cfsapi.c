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

/* read bytes from file *//* not done */
int cfs_read(struct cFS *cfs, char *buffer, char *path, int lim);

/* remove file *//* not done */
int cfs_remove_file(struct cFS *cfs, char *path);

/* shred & remove file *//* not done */
int cfs_sremove_file(struct cFS *cfs, char *path);

/* write bytes to file *//* not done */
int cfs_write(struct cFS *cfs, char *path, char *buffer, int lim);

void main(int argc, char *argv[]);
