/* cFS API */

#include <stdio.h>
#include "cfs.h"

#ifndef CFSAPI_H_
#define CFSAPI_H_

typedef FILE cFS;

/* close cFS */
#undef cfs_close
#define cfs_close(cfs) fclose(cfs)

/* open cFS */
#undef cfs_open
#define cfs_open(nodePath) fopen(nodePath, "r+")

/* create file */
int cfs_create_file(cFS *cfs, char *path);

/* read bytes from file */
int cfs_read(cFS *cfs, char *buffer, char *path, int lim);

/* remove file */
int cfs_remove_file(cFS *cfs, char *path);

/* shred & remove file */
int cfs_sremove_file(cFS *cfs, char *path);

/* write bytes to file */
int cfs_write(cFS *cfs, char *path, char *buffer, int lim);

#endif
