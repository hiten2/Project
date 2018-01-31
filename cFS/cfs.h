/* cFS macros & general layout */

#ifndef CFS_H_
#define CFS_H_

/* BEGIN BYTE ORDER */

/* first byte represents the number of bytes used to denote the disk size */
#undef CFS_SIZE_SIZE_B
#define CFS_SIZE_SIZE_B 0

/* second byte is where the disk size begins */
#undef CFS_SIZE_B
#define CFS_SIZE_B 1

/* then the key size */
#undef CFS_KEY_SIZE_B
#define CFS_KEY_SIZE_B(long_long_size) (CFS_SIZE_B + (long_long_size))

/* then the locking mechanism (for key verification upon first accessing cFS) */
#undef CFS_LOCK_SIZE
#define CFS_LOCK_SIZE 1024

#undef CFS_LOCK_B
#define CFS_LOCK_B(long_long_size) (CFS_KEY_SIZE(long_long_size) + (long_long_size))

/* size of the mapping */
#undef CFS_TREEMAP_SIZE
#define CFS_TREEMAP_SIZE 1048576

#undef CFS_TREEMAP_B
#define CFS_TREEMAP_B (CFS_LOCK_B(long_long_size) + CFS_LOCK_SIZE)

/* END BYTE ORDER */

/* header size */
#undef CFS_HEADER_SIZE
#define CFS_HEADER_SIZE(long_long_size) (CFS_TREEMAP_B + CFS_TREEMAP_SIZE)


/* minimum *usable* disk space required */
#undef CFS_MIN_STORAGE_SIZE
#define CFS_MIN_STORAGE_SIZE (4 * CFS_HEADER_SIZE)

#endif
