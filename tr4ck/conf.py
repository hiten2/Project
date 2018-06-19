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
import fcntl
import os

__doc__ = """configuration files"""

global DEFAULT_CONF_FLAVOR

class ConfFlavor:
    """
    rudimentary flavor for a configuration file

    note that when a comment evaluates to False (False, None, '', 0),
    we assume there are no comments
    """

    def __init__(self, assignment = ':', comment = '#'):
        assert not assignment == comment, "conflicting delimiters"
        self.assignment = assignment
        self.comment = comment

DEFAULT_CONF_FLAVOR = ConfFlavor()

class Conf(dict):
    """
    a basic configuration file reader/writer with dict-like behavior

    autosync specifies whether to automatically synchronize primary
    and secondary storage of the configuration file
    """

    def __init__(self, path = None, expect = None,
            flavor = DEFAULT_CONF_FLAVOR, autosync = True):
        dict.__init__(self)
        self.autosync = autosync

        if expect:
            expect = set(expect)
        self._expect = expect # the dictionary keys we should expect
        self.flavor = flavor
        self.path = path

        if self.path:
            self.read()

    def add(self, key, value):
        """
        add a key, value pair to the configuration file

        the key may already exist
        """
        if self.has_key(key):
            if not isinstance(self[key], list):
                dict.__setitem__(self, key, [self[key]])
            self[key].append(value)
        else:
            dict.__setitem__(self, key, value)

        if self.autosync:
            self.write()

    def clear(self):
        dict.clear(self)
        
        if self.autosync:
            self.write()

    def __delitem__(self, key):
        dict.__delitem__(self, key)

        if self.autosync:
            self.write()

    def load(self, string):
        """load from a string"""
        self.clear()
        lines = string.split('\n')
        
        if lines:
            for i in range(len(lines) - 1, -1, -1): # strip comments
                l = lines[i]

                if self.flavor.comment and self.flavor.comment in l:
                    l = l[:l.find(self.flavor.comment)]
                l = l.strip()

                if l:
                    lines[i] = l
                else:
                    del lines[i]

        for l in lines: # parse assignments
            k = l
            v = None

            if self.flavor.assignment in l:
                k, v = [e.strip() for e in l.split(self.flavor.assignment, 1)]
            self.add(k, v) # set/append as needed

        if self._expect and not self._expect == set(self.keys()):
            raise ValueError("missing and/or additional keys")

    def read(self):
        """load from path"""
        if not self.flavor or not self.path:
            raise ValueError("invalid flavor and/or path attribute")
        data = ''
        
        with open(self.path, "rb") as fp:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
            data = fp.read()
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
        self.load(data)

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)

        if self.autosync:
            self.write()

    def __str__(self):
        """convert to string"""
        lines = []

        for k, vs in self.items():
            k = str(k)

            if vs == None:
                lines.append(k)
                continue
            elif not isinstance(vs, list):
                vs = [vs]
            
            for v in vs:
                lines.append(k + self.flavor.assignment + ' ' + str(v))
        return '\n'.join(sorted(lines))

    def write(self, outpath = None):
        """write to path"""
        if not outpath:
            outpath = self.path

        with open(outpath, "wb") as fp:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
            fp.write(self.__str__())
            os.fdatasync(fp.fileno())
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
