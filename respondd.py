#!/usr/bin/env python3

import socketserver
import argparse
import socket
import struct
import json
import os
from zlib import compress

from gather import gather_data


def get_handler(directory, env):
    class ResponddUDPHandler(socketserver.BaseRequestHandler):
        @staticmethod
        def _get_provider_dir(provider):
            return os.path.join(directory, "{}.d".format(provider))

        def multi_request(self, providers):
            ret = {}
            for provider in providers:
                if '/' in provider:
                    continue
                try:
                    ret[provider] = gather_data(
                        self._get_provider_dir(provider),
                        env
                    )
                except:
                    pass
            return compress(str.encode(json.dumps(ret)))[2:-4]

        def handle(self):
            data = self.request[0].decode('UTF-8').strip()
            socket = self.request[1]
            response = None

            if data.startswith("GET "):
                response = self.multi_request(data.split(" ")[1:])
            elif '/' not in data:
                answer = gather_data(
                    self._get_provider_dir(data),
                    env
                )
                if answer:
                    response = str.encode(json.dumps(answer))

            if response:
                socket.sendto(response, self.client_address)

    return ResponddUDPHandler

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="""
      %(prog)s -h
      %(prog)s [-p <port>] [-g <group> -i <if0> [-i <if1> ..]] [-d <dir>]""")
    parser.add_argument('-p', dest='port',
                        default=1001, type=int, metavar='<port>',
                        help='port number to listen on (default 1001)')
    parser.add_argument('-g', dest='group',
                        default='ff02::2:1001', metavar='<group>',
                        help='multicast group (default ff02::2:1001)')
    parser.add_argument('-i', dest='mcast_ifaces',
                        action='append', metavar='<iface>',
                        help='interface on which the group is joined')
    parser.add_argument('-d', dest='directory',
                        default='.', metavar='<dir>',
                        help='data provider directory (default: $PWD)')
    parser.add_argument('-b', dest='batadv_ifaces',
                        action='append', metavar='<iface>',
                        help='batman-adv interface (default: bat0)')
    args = parser.parse_args()

    if not args.batadv_ifaces:
        args.batadv_ifaces = ['bat0']

    socketserver.ThreadingUDPServer.address_family = socket.AF_INET6
    server = socketserver.ThreadingUDPServer(
        ("", args.port),
        get_handler(args.directory, {'batadv_ifaces': args.batadv_ifaces})
    )

    if args.mcast_ifaces:
        group_bin = socket.inet_pton(socket.AF_INET6, args.group)
        for (inf_id, inf_name) in socket.if_nameindex():
            if inf_name in args.mcast_ifaces:
                mreq = group_bin + struct.pack('@I', inf_id)
                server.socket.setsockopt(
                    socket.IPPROTO_IPV6,
                    socket.IPV6_JOIN_GROUP,
                    mreq
                )

    server.serve_forever()
