import re
import socket

__doc__ = """login handlers"""

class LoginHandler:
    """interface for a login handler"""

    def __init__(self):
        pass

    def login(self, username, password):
        """actually log in"""
        raise NotImplementedError()
