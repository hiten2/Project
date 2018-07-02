# Copyright (C) 2018 Bailey Defino
# <http://hiten2.asuscomm.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import csv
import fcntl
import hashlib
import os
import StringIO
import sys

__doc__ = """a string-based database"""

def _help():
    print "a string-based database\n" \
          "Usage: python db.py [OPTIONS] DIRECTORY ACTION [NAME [DATA]]\n" \
          "OPTIONS\n" \
          "\t-h, --help\tshow this text and exit\n" \
          "DIRECTORY\n" \
          "\tthe database directory\n" \
          "ACTION\n" \
          "\tappend NAME [DATA]\tappend data to an entry\n" \
          "\tclean\tclean the database (if it exists)\n" \
          "\tcontains NAME\tdetermine whether an entry exists\n" \
          "\tdelete NAME\tdelete an entry\n" \
          "\tget NAME\tget an entry\n" \
          "\tinit\tinitialize the database (happens with all actions)\n" \
          "\tlist\tlist all entries as unicode-escaped strings\n" \
          "\tset NAME [DATA]\tset an entry\n" \
          "NAME\n" \
          "\tan entry name (a CSV string)\n" \
          "DATA\n" \
          "\tentry data (a string)"

class DB:
    """
    an extensible string-based database
    
    the database is made up of two main components:
    1. the database file
        a ragged CSV document where each row is a list of name components
    2. entries
        the corresponding raw data for an entry name,
        stored at "directory/subtree of hashed name components/entry.dat"

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
        self._db_reader = None
        self._db_writer = None
        self.directory = os.path.realpath(directory)
        hash = getattr(hashlib, hash)
        self._hash = lambda s: hash(str(s)).hexdigest()

    def append(self, name, data = ''):
        """append data to an entry (if it exists)"""
        self.__setitem__(name, data, "ab")

    def clean(self):
        """remove redundant/nonexistent entries from the database file"""
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
        path = self._generate_path(name)
        fp = open(path, "rb") # we need a lock
        
        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
        except IOError:
            locked = False
        
        try:
            os.unlink(path)

            while not path in ('', os.sep, self.directory) \
                    and not os.listdir(path):
                os.rmdir(path)
                path = os.path.dirname(path)
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
            self._db_reader = csv.reader(self._db_fp)
            self._db_writer = csv.writer(self._db_fp)
        return self

    def __exit__(self, *exception):
        if isinstance(self._db_fp, file):
            try:
                self._db_fp.close()
            except (IOError, OSError):
                pass

    def _generate_path(self, name):
        """return the hashed equivalent of a name"""
        if not isinstance(name, list) and not isinstance(name, tuple):
            name = [name]
        return os.path.join(os.path.realpath(self.directory),
            *([self._hash(str(n)) for n in name] + ["entry.dat"]))

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
        
        names = []

        try:
            self._db_fp.seek(0, os.SEEK_SET)
            
            for l in self._db_reader:
                if l in self:
                    names.append(l)
        except Exception as exception:
            pass
        
        if locked:
            try:
                fcntl.flock(self._db_fp.fileno(), fcntl.LOCK_UN)
            except IOError:
                pass

        if exception:
            raise exception
        return sorted(names)
    
    def _register(self, name):
        """register a name with the database (unlocked)"""
        self.__enter__()
        exception = None

        if not isinstance(name, list) and not isinstance(name, tuple):
            name = [name]
        
        try:
            self._db_writer.writerow(name)
            self._db_fp.flush()
            os.fdatasync(self._db_fp.fileno())
        except Exception as exception:
            pass

        if exception:
            raise exception
    
    def __setitem__(self, name, data, mode = "wb"):
        """
        store a name mapped to data
        
        this function is rather slow, as it calls
        both file.flush and os.fdatasync
        """
        self.__enter__()
        exception = None
        path = self._generate_path(name)

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        fp = open(path, mode)
        locked = True
        locked_fp = True

        try:
            fcntl.flock(self._db_fp.fileno(), fcntl.LOCK_EX)
        except IOError:
            locked = False

        try:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
        except IOError:
            locked_fp = False

        try:
            fp.write(data)
            fp.flush()
            os.fdatasync(fp.fileno())
            self._register(name)
        except Exception as exception:
            pass

        if locked_fp:
            try:
                fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
            except IOError:
                pass
        
        if locked:
            try:
                fcntl.flock(self._db_fp.fileno(), fcntl.LOCK_UN)
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
    
    if action in ("append", "contains", "delete", "get", "set"):
        if len(sys.argv) < 4:
            print "Missing entry name."
            _help()
            sys.exit()
        name = list(csv.reader(StringIO.StringIO(sys.argv[3])))[0]
        
        if action in ("append", "set") and len(sys.argv) > 4:
            data = sys.argv[4]
    elif not action in ("clean", "init", "list"):
        print "Invalid action."
        _help()
        sys.exit()
    db = DB(directory)
    db.__enter__()
    
    if action == "append":
        db.append(name, data)
    elif action == "clean":
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
            if not isinstance(n, list) and not isinstance(n, tuple):
                n = [n]
            csv.writer(sys.stdout).writerow(n)
            sys.stdout.flush()
    elif action == "set":
        db[name] = data
    # otherwise action == "init"
    db.__exit__()
