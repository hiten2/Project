/* cFS API handling */

#include <stdio.h>
#include "cfs.h"

#ifndef CFSIO_H_
#define CFSIO_H_

typedef FILE cFS;

/* close cFS */
#undef cfs_close
#define cfs_close(cfs) fclose(cfs)

/* open cFS */
#undef cfs_open
#define cfs_open(node) fopen(node, "r+");

/* create file */
int cfs_create_file(cFS *cfs, char *path);

/* dummy open file */
int cfs_open_file(cFS *cfs, char *path);

/* read bytes from file */
int cfs_read(cFS *cfs, char *buffer, char *path, int lim);

/* write bytes to file */
int cfs_write(cFS *cfs, char *path, char *buffer, int lim);

#endif
