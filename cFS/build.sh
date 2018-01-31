# bash build script
# requires: gcc

gcc mkfs.cfs.c cfs.c -o mkfs.cfs
chmod +x mkfs.cfs

gcc cfs.api.c cfs.c cfsapi.c -o cfs.api
chmod +x cfs.api
