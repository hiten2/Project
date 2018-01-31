#include <stdio.h>
#include <stdlib.h>
#include "cfs.h"
#include "cfsapi.h"

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
    for (int i = 0; i < argc; make_cfs(argv[i++]));
  }
}
