/* cFS API */

#include "cfsapi.h"

/* create file */
int cfs_create_file(cFS *cfs, char *path);

/* dummy open file */
int cfs_open_file(cFS *cfs, char *path);

/* read bytes from file */
int cfs_read(cFS *cfs, char *buffer, char *path, int lim);

/* write bytes to file */
int cfs_write(cFS *cfs, char *path, char *buffer, int lim);
