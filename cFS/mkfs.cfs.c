/* mkfs utility for cFS */

#define NOAUTO

#include <stdio.h>
#include "cfs.h"
#include "cfsapi.h"

void main(int argc, char *argv[]) {
  if (argc > 1) {
    for (int i = 0; i < argc; cfs_make(argv[i++]))
      printf("Making cFS on %s....\n", argv[i]);
  }
}
