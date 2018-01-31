/* cFS */

#include "cfs.h"

/* get cFS long long size */
int cfs_get_long_long_size(char *nodePath) {
  cFS *node;
  int size;
  size = 0;
  
  if (nodePath != NULL && (node = fopen(nodePath, "rb")) != NULL) {
    char buffer[1];
    fread(buffer, 1, 1, node);
    fclose(node);
    size = (int) buffer[0];
  }
  return size;
}
