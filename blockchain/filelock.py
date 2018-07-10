import fcntl

class FileLock:
    """
    an flock-oriented enterable for clarity

    if complain evaluates to True, raise any pertinent errors
    """

    def __init__(self, fp, complain = False):
        self.complain = complain
        self.fp = fp
        self.locked = False

    def __enter__(self):
        try:
            fcntl.flock(self.fp.fileno(), fcntl.LOCK_EX)
            self.locked = True
        except IOError as e:
            if self.complain:
                raise e
        return self

    def __exit__(self, *exception):
        if self.locked:
            try:
                fcntl.flock(self.fp.fileno(), fcntl.LOCK_UN)
            except IOError as e:
                if self.complain:
                    raise e
        elif self.complain:
            raise IOError("already unlocked")
