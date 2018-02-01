#include <stdio.h>
#include "cfs.h"
#include "cfsapi.h"

/* mkfs utility for cFS */

void main(int argc, char *argv[]) {
  if (argc > 1) {
    for (int i = 0; i < argc; cfs_make(argv[i++]))
      printf("Making cFS on %s....\n", argv[i]);
  }
}
