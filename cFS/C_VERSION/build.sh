# bash build script
# requires: gcc

gcc mkfs.cfs.c cfs.c -o mkfs.cfs
chmod +x mkfs.cfs

gcc cfsapi.c cfs.c -o cfsapi
chmod +x cfs.api
