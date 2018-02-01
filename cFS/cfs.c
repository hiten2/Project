/* cFS */

#include "cfs.h"

/* extract next cFS entry position *//* not done */
long long cfs_entry_extract_next(struct cFS *cfs, struct cFSEntry *entry) {
  if (cfs != NULL && cfs->size != NULL && entry->content != NULL)
    return (long long) entry->content[0];
  return -1;
}

/* extract previous cFS entry position */
long long cfs_entry_extract_prev(struct cFSEntry *entry);

/* extract cFS entry type */
int cfs_entry_extract_type(struct cFSEntry *entry);

/* get cFS long long size */
int cfs_get_long_long_size(struct cFS *cfs) {
  int size;
  size = 0;
  
  if (cfs->node != NULL) {
    char buffer[1];
    fread(buffer, 1, 1, cfs->node);
    fseek(cfs->node, -1, SEEK_CUR);
    size = (int) buffer[0];
  }
  return size;
}

/* get cFS node size */
int cfs_get_size(struct cFS *cfs);

/* resolve cFS path to a byte position */
long long cfs_resolve_path(struct cFS *cfs, char *path);

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
