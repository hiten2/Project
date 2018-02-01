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

/* resolve cFS path to a byte position *//* not done */
long long cfs_resolve_path(struct cFS, char *path);

/* deletion */
void del_cfs(struct cFS *cfs) {
  if (cfs != NULL) {
    fclose(cfs->node);
    free(cfs);
    cfs = NULL;
  }
}

/* initialization *//* not done */
struct cFS *init_cfs(char *nodePath, char *key, long long keySize);
