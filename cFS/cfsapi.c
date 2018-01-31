/* cFS API */

#include "cfsapi.h"

/* create file *//* not done */
int cfs_create_file(cFS *cfs, char *path) {
  if (cfs != NULL && path != NULL) {
    /* pass */
    return 1;
  }
  return 0;
}

/* read bytes from file *//* not done */
int cfs_read(cFS *cfs, char *buffer, char *path, int lim);

/* write bytes to file *//* not done */
int cfs_write(cFS *cfs, char *path, char *buffer, int lim);
