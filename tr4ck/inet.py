import os
import uuid

"""
internet utilities

note that all MAC addresses are in hexadecimal form
and IP addresses are in dot-decimal form
"""

def get_active_device():
    """use "ip link" to detect the active device"""
    descriptors = [d[0] for d in _split_ip_cmd("ip link")]

    for d in descriptors:
        d = [e for e in d.split(' ') if e]
        
        if d[8].lower() == "up":
            return d[1][:-1]
    return

def get_hwaddr():
    """return the hardware address"""
    return ltomac(uuid.getnode())

def get_ip(device = None):
    """use "ip address" to get the IP address (without the subnet)"""
    if not device:
        device = get_active_device()
    descriptors = _split_ip_cmd("ip address")

    for d in descriptors:
        if len(d) < 3:
            continue
        curdev = d[0].split(' ')[1][:-1]
        
        if curdev == device:
            return strip_subnet([e.strip() for e in d[2].split(' ')
                if e.strip()][1])
    return

def get_mac(device = None):
    """use "ip link" to detect the MAC address for a device"""
    if not device:
        device = get_active_device()
    descriptors = _split_ip_cmd("ip link")
    
    for d in descriptors:
        if len(d) < 2:
            continue
        curdev = d[0].split(' ')[1][:-1]
        
        if curdev == device:
            return [e.strip() for e in d[1].split(' ') if e.strip()][1]
    return

def ltomac(mac):
    """convert a long into a formatted MAC address"""
    mac = hex(mac)[2:].rstrip('L') # remove "0x...L"
    return ':'.join((mac[i:i + 2] for i in range(0, len(mac), 2)))

def new_mac(device = None):
    """return a new MAC address for a device"""
    if not device:
        device = get_active_device()
    mac = random_mac()
    omit = [get_hwaddr(), get_mac()]

    while mac in omit:
        mac = random_mac()
    return mac

def random_mac():
    """return a cryptographically secure random MAC address"""
    num = 0L
    preserve = int(get_hwaddr().split(':', 1)[0], 16) & 3

    for i, b in enumerate(os.urandom(6)):
        num += ord(b) * (256 ** i)
    first, rest = ltomac(num).split(':', 1)
    first = int(first, 16)
    first = (first & 252) | preserve
    return ':'.join((hex(first)[2:], rest))

def reset_mac(device = None):
    """reset the MAC address for a device"""
    if not device:
        device = get_active_device()
    return set_mac(device, get_hwaddr()) # uses the real address

def set_mac(device = None, mac = None):
    """
    set the MAC address for a device
    when the MAC address is omitted, a random one is used
    return the new address or False
    """
    if not device:
        device = get_active_device()
    
    if not mac:
        mac = new_mac()
    cmd_fmt = """ip link set {device} down
        ip link set {device} address {mac}
        ip link set {device} up"""

    if not os.system(cmd_fmt.format(device = device, mac = mac)):
        return mac
    return False

def _split_ip_cmd(cmd):
    """
    split one of the "ip" variety commands by device descriptors
    return a list of lines per descriptor
    """
    lines = []

    with os.popen(cmd) as stdout:
        lines = stdout.readlines()
    descriptors = []

    for i, l in enumerate(lines): # split lines by device descriptors
        if l and not l[0].isspace():
            descriptors.append([])
        descriptors[-1].append(l)
    return descriptors

def strip_subnet(ip):
    """remove the subnet from an IP address string"""
    if '/' in ip:
        return ip[:ip.find('/')]
    return ip
