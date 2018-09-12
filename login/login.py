import re

__doc__ = """login handlers"""

def _default_check_fail(telnet_lines):
    """check for a basic failure message in some lines of telnet data"""
    return len(re.findall("([^a-zA-Z]|^)(F|f)ail([^a-zA-Z]|$)",
        telnet_lines.lower())) > 0

class LoginHandler:
    """interface for a login handler"""

    def __init__(self):
        pass

    def login(self, username, password):
        """actually log in"""
        raise NotImplementedError()
