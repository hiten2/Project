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
          "\delete NAME\tdelete an entry\n" \
          "\tget NAME\tget an entry\n" \
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
    """

    def __init__(self, directory = os.getcwd(), enter = True, hash = "sha256"):
        self._db_fp = None
        self._db_path = os.path.join(directory, "db.csv")
        self.directory = directory
        hash = getattr(hashlib, hash)
        self._hash = lambda s: hash(str(s)).hexdigest()
        
        if enter:
            self.__enter__()

    def clean(self):
        """clean "db.csv" of redundant/non-existent entries"""
        locked = True
        
        try:
            fcntl.flock(self._db_fp.fileno(), fcntl.LOCK_EX)
        except IOError:
            locked = False
        names = self.list(self._db_fp)
        self._db_fp.seek(0, os.SEEK_SET)

        try:
            self._db_fp.truncate()
        except (IOError, OSError):
            raise OSError("failed to truncate database")
        
        try:
            for n in names:
                self._register(n)
        except (IOError, OSError):
            raise OSError("failed to rewrite database")

        if locked:
            try:
                fcntl.flock(self._db_fp.fileno(), fcntl.LOCK_EX)
            except IOError:
                pass
    
    def __contains__(self, name):
        """return whether an entry exists"""
        return os.path.exists(self._generate_path(name))

    def __del__(self):
        self.__exit__()

    def __delitem__(self, name):
        fp = None
        locked = True
        
        if not name in self:
            return

        try:
            fp = open(self._generate_path(name), "rb")
        except (IOError, OSError): # unknown error
            raise OSError("can't open entry for deletion")
        
        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
        except IOError:
            locked = False
        
        try:
            os.unlink(self._generate_path(name))
        except OSError:
            raise OSError("failed to delete entry")
        self.clean()

        if locked:
            try:
                fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
            except IOError:
                pass

        try:
            fp.close()
        except (IOError, OSError):
            pass
    
    def __enter__(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        if not self._db_fp or self._db_fp.closed:
            self._db_fp = open(self._db_path, "a+b")

    def __exit__(self):
        if self._db_fp:
            try:
                self._db_fp.close()
            except (IOError, OSError):
                pass

    def _generate_path(self, name):
        """return the hashed equivalent of a name"""
        return os.path.join(self.directory, self._hash(name))

    def __getitem__(self, name):
        """retrieve data"""
        data = None
        fp = None
        locked = True
        path = self._generate_path(name)
        
        if not name in self:
            raise ValueError("no such entry")
        elif not os.access(path, os.R_OK):
            raise OSError("entry unreadable")

        try:
            fp = open(path, "rb")
        except (IOError, OSError): # unknown error
            raise OSError("can't open entry")

        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
        except IOError:
            locked = False

        try:
            data = fp.read()
        except (IOError, OSError): # unknown error
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

        if data == None:
            raise OSError("failed to read entry")
        return data

    def list(self, fp = None):
        """
        return a list of all the entries (names only)
        
        this function only locks when fp is None
        """
        locked = False
        opened = fp == None

        if opened:
            try:
                fp = open(self._db_path, "rb")
            except (IOError, OSError):
                raise OSError("failed to open database")

            try:
                fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
                locked = True
            except IOError:
                pass
        names = set()

        try:
            for l in fp.readlines():
                if l.endswith("\r\n"):
                    l = l[:-2]
                elif l.endswith('\n'):
                    l = l[:-1]
                l = l.decode("unicode-escape")
                
                if l in self:
                    names.add(l)
        except (IOError, OSError): # unknown error
            raise OSError("failed to read database")

        if opened:
            if locked:
                try:
                    fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
                except IOError:
                    pass
            
            try:
                fp.close()
            except (IOError, OSError):
                pass
        return sorted(names)
    
    def _register(self, name):
        """register a name with the database"""
        try:
            self._db_fp.write(name.encode("unicode-escape"))
            self._db_fp.write("\r\n")
            os.fdatasync(self._db_fp.fileno())
        except (AttributeError, IOError, OSError):
            raise OSError("registration failed")
    
    def __setitem__(self, name, data):
        """store a name mapped to data"""
        fp = None
        locked = True
        path = self._generate_path(name)
        
        try:
            fp = open(path, "wb")
        except (IOError, OSError): # unknown error
            raise OSError("can't open entry")

        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
        except IOError:
            locked = False

        try:
            fp.write(data)
            os.fdatasync(fp.fileno())
        except (IOError, OSError): # unknown error
            raise OSError("failed to write entry")
        self._register(name)
        
        if locked:
            try:
                fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
            except IOError:
                pass
        
        try:
            fp.close()
        except (IOError, OSError):
            pass

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
    elif not action in ("clean", "list"):
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
    db.__exit__()
