import socket


__all__ = [
    'AF_INET',
    'AF_INET6',
    'SOCK_TCP',
    'SHUT_RD',
    'SHUT_WR',
    'SHUT_RDWR',
]

AF_INET = socket.AF_INET
AF_INET6 = socket.AF_INET6
SOCK_TCP = socket.SOCK_STREAM
SOCK_UDP = socket.SOCK_DGRAM

SHUT_RD = 0
SHUT_RDWR = 2
SHUT_WR = 1
