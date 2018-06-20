# Bailey Defino 2018
# <http://hiten2.asuscomm.com>

# CLARIFICATIONS:
#   1. "Authorship Information" regards the following:
#      "Bailey Defino," the year, and "<http://hiten2.asuscomm.com>."
#   2. "Illegal Activity" refers to any activity that falls outside
#       of the laws applicable to the end user.
#   3. "Negative Consequences" are defined by the original author;
#       they include, but are not limited to: illegal activity
#       and property damage.
#   4. "Original Author" refers to the author behind the "Bailey Defino"
#       alias.
#   5. "This License" and "License" refer to the following as they appear
#       on a verbatim copy of this code: authorship information
#       and complete sections entitled: "CLARIFICATIONS," "DISCLAIMER,"
#       "DISTRIBUTION CONDITIONS," and "LICENSE."

# DISCLAIMER:
#   THIS CODE IS PROVIDED WITH NO WARRANTY NOR ANY GAURANTEES.
#  THE ORIGINAL AUTHOR IS NOT RESPONSIBLE FOR ANY NEGATIVE CONSEQUENCES
#   RESULTING FROM ANY ACTION PERFORMED ON OR WITH THE FOLLOWING CODE,
#   REGARDLESS OF WHETHER IT IS A VERBATIM COPY.

# DISTRIBUTION CONDITIONS:
#   (1) The distributed code contains this license,
#   (2) AND either "a" OR "b":
#     (a) the distributed code is a verbatim copy,
#     (b) OR the distributed code asserts that the original author was NOT
#         responsible for any modifications in the distributed code.
#   (3) the distributed code comes without a charge: monetary or otherwise.

# LICENSE:
#   This verbatim code is intellectual property, but is also free
#   and open source software.  This code, verbatim or modified, may only
#   be distributed if ALL of the distribution conditions are met.
#   If not distributed, this code may be modified in any way;
#   however, modification of this code and/or license,
#   does NOT void this original license.

__doc__ = """a string-based database"""

import fcntl
import hashlib
import os
import sys

def _help():
    print "a string-based database\n" \
          "Usage: python db.py [OPTIONS] DIRECTORY ACTION [NAME [DATA]]\n" \
          "OPTIONS\n" \
          "\t-h, --help\tshow this text and exit\n" \
          "DIRECTORY\n" \
          "\tthe database directory\n" \
          "ACTION\n" \
          "\tclean\tclean the database (if it exists)\n" \
          "\tcontains NAME\tdetermine whether an entry exists\n" \
          "\tdelete NAME\tdelete an entry\n" \
          "\tget NAME\tget an entry\n" \
          "\tinit\tinitialize the database with \"db.csv\" (default)\n" \
          "\tlist\tlist all entries as unicode-escaped strings\n" \
          "\tset NAME [DATA]\tset an entry\n" \
          "NAME\n" \
          "\tan entry name (a string)\n" \
          "DATA\n" \
          "\tentry data (a string)"

class DB:
    """
    an extensible string-based database
    
    the database is made up of two main components:
    1. the database file
        a (CR)LF-separated list of unicode-escaped entry names
        which MAY or MAY NOT exist
    2. entries
        the corresponding raw data for an entry name,
        stored at "directory/hashed-entry-name"

    the database model is dict-like, but is intended for extensibility
    through its simplicity
    
    the functions follow a simple model for integrity purposes:
    1. enter as needed
    2. open any files
    3. lock files
    4. save any exceptions during the operation
    5. unlock files
    6. close any files
    7. raise any exceptions
    8. return any data
    """

    def __init__(self, directory = os.getcwd(), hash = "sha256"):
        self._db_fp = None
        self._db_path = os.path.join(directory, "db.csv")
        self.directory = directory
        hash = getattr(hashlib, hash)
        self._hash = lambda s: hash(str(s)).hexdigest()

    def clean(self):
        """clean "db.csv" of redundant/non-existent entries"""
        self.__enter__()
        exception = None
        locked = True
        
        try:
            fcntl.flock(self._db_fp.fileno(), fcntl.LOCK_EX)
        except IOError:
            locked = False
        
        try:
            names = self.list()
            self._db_fp.seek(0, os.SEEK_SET)
            self._db_fp.truncate()

            for n in names:
                self._register(n)
        except Exception as exception:
            pass
        
        if locked:
            try:
                fcntl.flock(self._db_fp.fileno(), fcntl.LOCK_EX)
            except IOError:
                pass

        if exception:
            raise exception
    
    def __contains__(self, name):
        """return whether an entry exists (not whether it's in the database)"""
        return os.path.exists(self._generate_path(name))

    def __del__(self):
        self.__exit__()

    def __delitem__(self, name):
        """delete an entry"""
        exception = None
        locked = True
        fp = open(self._generate_path(name), "rb") # we need a lock
        
        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
        except IOError:
            locked = False
        
        try:
            os.unlink(self._generate_path(name))
            self.clean()
        except Exception as exception:
            pass
        
        if locked:
            try:
                fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
            except IOError:
                pass

        try:
            fp.close()
        except (IOError, OSError):
            pass

        if exception:
            raise exception
    
    def __enter__(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        if not isinstance(self._db_fp, file) or self._db_fp.closed:
            self._db_fp = open(self._db_path, "a+b")
        return self

    def __exit__(self, *exception):
        if isinstance(self._db_fp, file):
            try:
                self._db_fp.close()
            except (IOError, OSError):
                pass

    def _generate_path(self, name):
        """return the hashed equivalent of a name"""
        return os.path.join(self.directory, self._hash(name))

    def __getitem__(self, name):
        """retrieve an entry"""
        data = ''
        exception = None
        fp = open(self._generate_path(name), "rb")
        locked = True

        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
        except IOError:
            locked = False

        try:
            data = fp.read()
        except Exception as exception:
            pass
        
        if locked:
            try:
                fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
            except IOError:
                pass
        
        try:
            fp.close()
        except (IOError, OSError):
            pass
        
        if exception:
            raise exception
        return data

    def list(self):
        """return an unsorted list of all the entries (names only)"""
        self.__enter__()
        exception = None
        locked = True
        
        try:
            fcntl.flock(self._db_fp.fileno(), fcntl.LOCK_EX)
        except IOError:
            locked = False
        names = set()

        try:
            self._db_fp.seek(0, os.SEEK_SET)
            
            for l in self._db_fp.readlines():
                if l.endswith("\r\n"):
                    l = l[:-2]
                elif l.endswith('\n'):
                    l = l[:-1]
                l = l.decode("unicode-escape")
                
                if l in self:
                    names.add(l)
        except Exception as exception:
            pass
        
        if locked:
            try:
                fcntl.flock(self._db_fp.fileno(), fcntl.LOCK_UN)
            except IOError:
                pass

        if exception:
            raise exception
        return list(names)
    
    def _register(self, name):
        """register a name with the database"""
        self.__enter__()
        exception = None
        
        try:
            self._db_fp.write(name.encode("unicode-escape"))
            self._db_fp.write("\r\n")
            self._db_fp.flush()
            os.fdatasync(self._db_fp.fileno())
        except Exception as exception:
            pass

        if exception:
            raise exception
    
    def __setitem__(self, name, data):
        """
        store a name mapped to data
        
        this function is rather slow, as it calls
        both file.flush and os.fdatasync
        """
        self.__enter__()
        exception = None
        fp = open(self._generate_path(name), "wb")
        locked = True

        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
        except IOError:
            locked = False

        try:
            fp.write(data)
            fp.flush()
            os.fdatasync(fp.fileno())
            self._register(name)
        except Exception as exception:
            pass
        
        if locked:
            try:
                fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
            except IOError:
                pass
        
        try:
            fp.close()
        except (IOError, OSError):
            pass
        
        if exception:
            raise exception

if __name__ == "__main__":
    action = None
    data = ''
    db = None
    directory = None
    name = None
    
    if len(sys.argv) < 3:
        _help()
        sys.exit()

    for arg in sys.argv[1:]:
        if arg in ("-h", "--help"):
            _help()
            sys.exit()
    directory, action = sys.argv[1:3]
    action = action.lower()
    
    if action in ("contains", "delete", "get", "set"):
        if len(sys.argv) < 4:
            print "Missing entry name."
            _help()
            sys.exit()
        name = sys.argv[3]
        
        if action == "set" and len(sys.argv) > 4:
            data = sys.argv[4]
    elif not action in ("clean", "init", "list"):
        print "Invalid action."
        _help()
        sys.exit()
    db = DB(directory)
    
    if action == "clean":
        db.clean()
    elif action == "contains":
        print name in db
    elif action == "delete":
        del db[name]
    elif action == "get":
        sys.stdout.write(db[name])
        sys.stdout.flush()
    elif action == "list":
        for n in db.list():
            print n.encode("unicode-escape")
    elif action == "set":
        db[name] = data
    # otherwise, action == "init"
    db.__exit__()
