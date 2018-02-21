"""dummy cipher"""

__package__ = "cfs"

import cipherinterface

class DummyCipher(cipherinterface.CipherInterface):
    def __init__(self, *args, **kwargs):
        cipherinterface.CipherInterface.__init__(self)

    def decipher(self, s, *args, **kwargs):
        return s

    def encipher(self, s, *args, **kwargs):
        return s
