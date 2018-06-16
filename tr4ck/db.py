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

"""basic web database management"""

import csv
import fcntl
import hashlib
import os
import thread
import time

class DB:
    """
    an extensible SHA-256-based database
    
    when storage is specified, directory/db.csv's rows resemble:
    "unicode-escaped ID, SHA-256"
    where SHA-256 represents the resource subdirectory,
    and entries in directory/SHA-256 are timestamped (accurate to the second)
    e.g. at timestamp T, ID's data is in "directory/SHA-256/T"

    this path structure can be taken advantage of:
    store can be called with anything as a timestamp
    e.g. store(data, id, "data.txt") could store data
    into "directory/SHA-256/data.txt"

    this string-based structure could also be taken advantage
    of in order to represent sub-databases
    e.g. entry "A.1.name"
    could represent database 'A''s entry '1''s "name" value

    concurrency-safe across multiple threads and processes

    existence of a record is contingent upon BOTH its presence in the
    database file and its existence on-disk
    """#######################ensure parallel safety
    ##############fix encoding issues

    def __init__(self, directory = os.getcwd(), db_mode = "ab",
            concurrent = True):
        self.concurrent = concurrent
        self._db_csv = os.path.join(directory, "db.csv")
        self._db_csv_fp = None
        self._db_csv_writer = None
        self.db_mode = db_mode
        self._decodeid = lambda i: str(i).decode("unicode-escape")
        self.directory = directory
        self._encodeid = lambda i: str(i).encode("unicode-escape")
        
        self.__enter__()

    def __del__(self):
        self.__exit__()
    
    def __enter__(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        opened = not self._db_csv_fp
        
        if opened:
            self._db_csv_fp = open(self._db_csv, self.db_mode)

        if opened or not self._db_csv_writer:
            self._db_csv_writer = csv.writer(self._db_csv_fp)

        with open(self._db_csv, "rb") as _fp:
            if not _fp.readline(): # write header
                self._db_csv_writer.writerow(("unicode-escaped-id", "sha-256"))
        return self

    def exists(self, id, timestamp = None):
        """return whether an entry exists and is non-empty"""
        id = self._encodeid(id)
        timestamps = self.timestamps(id)

        if timestamp:
            return timestamp in timestamps
        return not not timestamps

    def __exit__(self):
        if self._db_csv_fp:
            self._db_csv_fp.close()

    def _generate_directory(self, id):
        """generate the local directory for a ID"""
        id = self._encodeid(id)
        return os.path.join(self.directory, self._hash_id(id))
    
    def _generate_path(self, id, timestamp = None):
        """generate the local, timestamped path for a ID"""
        id = self._encodeid(id)
        
        if not timestamp:
            timestamp = time.time()
        return os.path.join(self._generate_directory(id), str(timestamp))

    def _hash_id(self, id):
        """return a SHA-256 hash for a ID"""
        id = self._encodeid(id)
        return hashlib.sha256(id).hexdigest()
    
    def _register(self, id):
        """
        add a ID to the CSV database
        a call to this function implies that an entry for ID already exists

        note that there is no cross-validation, so there may be repeats
        in "db.csv"
        """
        id = self._encodeid(id)
        _dir = self._generate_directory(id)
        _hash = os.path.basename(_dir)
        
        if self.concurrent:
            fcntl.flock(self._db_csv_fp.fileno(), fcntl.LOCK_EX)
        self._db_csv_writer.writerow((id, _hash))
        self._db_csv_fp.flush()

        if self.concurrent:
            fcntl.flock(self._db_csv_fp.fileno(), fcntl.LOCK_UN)

    def retrieve(self, id, timestamp = None):
        """
        retrieve data on a ID, optionally with a specific timestamp
        if no timestamp is provided, the last entry will be used
        """
        data = None
        _exception = None
        id = self._encodeid(id)
        timestamp = str(timestamp)
        timestamps = self.timestamps(id)
        
        if not timestamps or (timestamp and not timestamp in timestamps):
            return
        elif not timestamp:
            timestamp = timestamps[-1]
        _path = self._generate_path(id, timestamp)
        _dir = os.path.dirname(_path)

        if not _path:
            return
        _fp = open(_path, "rb")

        if self.concurrent:
            fcntl.flock(_fp.fileno(), fcntl.LOCK_EX)
        
        try:
            data = _fp.read()
        except Exception as _exception:
            pass

        if self.concurrent:
            fcntl.flock(_fp.fileno(), fcntl.LOCK_UN)
        _fp.close()

        if _exception:
            raise _exception
        return data

    def store(self, data, id, timestamp = None, mode = "wb"):
        """store ID data and return the timestamp"""
        _exception = None
        id = self._encodeid(id)
        _path = self._generate_path(id, timestamp)
        _existed = os.path.exists(_path)
        _dir = os.path.dirname(_path)

        if not os.path.exists(_dir):
            os.makedirs(_dir)
        _fp = open(_path, mode)

        if self.concurrent:
            fcntl.flock(_fp.fileno(), fcntl.LOCK_EX)

        try:
            if not isinstance(data, bytearray) and not isinstance(data, bytes):
                data = bytearray(data)
            _fp.write(data)
        except Exception as _exception:
            pass

        if self.concurrent:
            fcntl.flock(_fp.fileno(), fcntl.LOCK_UN)
        _fp.close()

        if _exception:
            raise _exception

        if not _existed:
            self._register(id)
        return os.path.basename(_path) # refers to timestamp

    def timestamps(self, id):
        """return the sorted, recorded timestamps for a ID"""
        id = self._encodeid(id)
        _dir = self._generate_directory(id)
        
        if os.path.exists(_dir):
            return sorted(os.listdir(_dir))
        return []

    def ids(self):
        """return a list of IDs stored in the database"""
        _fp = open(self._db_csv, "rb")
        _fp_reader = csv.reader(_fp)

        if self._concurrent:
            fcntl.flock(_fp.fileno(), fcntl.LOCK_EX)
        ids = list(_fp_reader)

        if self._concurrent:
            fcntl.flock(_fp.fileno(), fcntl.LOCK_UN)
        _fp.close()
        return [self._decodeid(i) for i in ids]
