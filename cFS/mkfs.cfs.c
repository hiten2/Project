#include <stdio.h>
#include <stdlib.h>
#include "cfs.h"

/* mkfs utility for cFS */

/* return file size */
unsigned long getfsize(FILE *fp) {
  if (fp != NULL) {
    unsigned long int cur = ftell(fp);
    fseek(fp, 0, SEEK_END);
    size = ftell(fp);
    fseek(fp, cur, SEEK_SET);
  }
  return 0;
}

void main(int argc, char *argv[]) {
  if (argc > 1) {
    for (int i = 0; i < argc; mkfs_cfs(argv[i++]));
  }
}

/* make cFS *//* not done */
int mkfs_cfs(char *nodePath) {
  FILE *node;
  unsigned long size;
  
  if ((node = fopen(nodePath, "wb")) != NULL && (size = get_fsize(node)) > CFS_MIN_STORAGE_SIZE) {
    fwrite((char) sizeof(long long), 1, node); /* byte 1 = size of size block */
    fwrite(size, sizeof(long long), 1, node); /*bytes 2-size of size block = size of storage medium */
    fwrite(key_size, 1, sizeof(long long), node);
    int i;
    
    for (i = 0; i < CFS_LOCK_SIZE; fwrite(i++ % 512, 1, 1, node));
    
    for (i = 0; i < CFS_TREEMAP_SIZE; fwrite('\0', 1, 1, node), i++); /* initialize tree mapping portion */
}
