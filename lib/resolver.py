import socket
import struct
import fcntl


def resolve(iface=None):
    if iface is None:
        iface = 'eth0'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd = sock.fileno()
    SIOCGIFADDR = 0x8915
    ifreq = struct.pack('16sH14s', iface, socket.AF_INET, '\x00'*14)
    try:
         res = fcntl.ioctl(sockfd, SIOCGIFADDR, ifreq)
    except:
         return None
    ip = struct.unpack('16sH2x4s8x', res)[2]
    return socket.inet_ntoa(ip)

