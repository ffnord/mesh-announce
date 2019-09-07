import ctypes
import socket
from socketserver import ThreadingUDPServer

class in6_addr_U(ctypes.Union):
    _fields_ = [
        ('__u6_addr8', ctypes.c_uint8 * 16),
        ('__u6_addr16', ctypes.c_uint16 * 8),
        ('__u6_addr32', ctypes.c_uint32 * 4),
    ]


class in6_addr(ctypes.Structure):
    _fields_ = [
        ('__in6_u', in6_addr_U),
    ]

class in6_pktinfo(ctypes.Structure):
    _fields_ = [
        ('ipi6_addr', in6_addr),
        ('ipi6_ifindex', ctypes.c_uint),
    ]

class MetadataUDPServer(ThreadingUDPServer):
    def __init__(self, *args, **kwargs):
        super(MetadataUDPServer, self).__init__(*args, **kwargs)
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_RECVPKTINFO, 1)

    def get_request(self):
        data, anc_data, _, client_addr = self.socket.recvmsg(self.max_packet_size, socket.CMSG_SPACE(65535))
        ifindex = None
        for anc_record in anc_data:
            (anc_level, anc_type, anc_datum) = anc_record
            if anc_level == socket.IPPROTO_IPV6 and anc_type == socket.IPV6_PKTINFO:
                pktinfo = in6_pktinfo.from_buffer_copy(anc_datum)
                ifindex = pktinfo.ipi6_ifindex
        return (data, self.socket, ifindex), client_addr

