# cFS (a basic encrypted filesystem)
## development plan
1. solidify `diskutil.py` to be able to perform disk-related operations and atol/ltoa conversions
2. finish `diskdll.py`, and make sure that it is able to store a doubly linked list on disk
3. determine a logical structure for a cFS object and its encryption standard, then optimize it for efficiency
4. compile using Cython into a shared object library
