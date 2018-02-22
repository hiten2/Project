"""preserved I/O"""

__package__ = "cfs"

import os

class PreservedIO:
    def __init__(self, f, pos):
        assert isinstance(f, file) and not f.closed, "f must be an open \'file\'"
        assert type(pos) in (int, long) and pos >= 0, "pos must be a non-negative integer"
        self.f = f
        self.pos = pos
        self._start = self.f.tell()

    def __enter__(self):
        """seek"""
        self._start = self.f.tell()
        self.f.seek(self.pos, os.SEEK_SET)

    def __exit__(self):
        """reseek"""
        self.f.seek(self._start, os.SEEK_SET)
    
    def func(self, func, *args, **kwargs):
        """execute a function at the position and reseek"""
        self.__enter__()
        v = self._raw_func(func, *args, **kwargs)
        self.__exit__()
        return v

    def _raw_func(self, func, *args, **kwargs):
        """execute a function"""
        try:
            return func(self.f, *args, **kwargs)
        except Exception as e:
            raise e
