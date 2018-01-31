/* cFS API */

#include <stdio.h>
#include "cfs.h"

#ifndef CFSAPI_H_
#define CFSAPI_H_

/* close cFS */
#undef cfs_close
#define cfs_close(cfs) fclose(cfs->node)

/* open cFS */
#undef cfs_open
#define cfs_open(nodePath) fopen(nodePath, "r+")

/* cFS outline */
struct cFS {
  char *key;
  long keySize;
  FILE *node;
};

/* create file */
int cfs_create_file(struct cFS *cfs, char *path);

/* read bytes from file */
int cfs_read(struct cFS *cfs, char *buffer, char *path, int lim);

/* remove file */
int cfs_remove_file(struct cFS *cfs, char *path);

/* shred & remove file */
int cfs_sremove_file(struct cFS *cfs, char *path);

/* write bytes to file */
int cfs_write(struct cFS *cfs, char *path, char *buffer, int lim);

#endif
