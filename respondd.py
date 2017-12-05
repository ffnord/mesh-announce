#!/usr/bin/env python3

import socketserver
import argparse
import socket
import struct
import json
import os
import threading
import time
from zlib import compress

import netifaces
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


def listen(iface, group, port, directory, env):
    # multicast
    print("binding to {0}%{1} port {2}...".format(
        group, iface, port)
    )
    mcast_server = socketserver.ThreadingUDPServer(
        (group, port, 0, socket.if_nametoindex(iface)),
        get_handler(directory, env)
    )

    group_bin = socket.inet_pton(socket.AF_INET6, group)
    mreq = group_bin + struct.pack('@I', socket.if_nametoindex(iface))
    mcast_server.socket.setsockopt(
        socket.IPPROTO_IPV6,
        socket.IPV6_JOIN_GROUP,
        mreq
    )

    threading.Thread(target=mcast_server.serve_forever).start()

    # unicast
    lladdrs = [
        item['addr']
        for item
        in netifaces.ifaddresses(iface).get(socket.AF_INET6, [])
        if item['addr'].startswith('fe80::')
    ]

    for lladdr in lladdrs:
        print("binding to {0}%{1} port {2}...".format(
            lladdr, iface, port)
        )
        ucast_server = socketserver.ThreadingUDPServer(
            (lladdr, port, 0, socket.if_nametoindex(iface)),
            get_handler(args.directory, env)
        )
        threading.Thread(target=ucast_server.serve_forever).start()

    return socket.if_nametoindex(iface), [mcast_server, ucast_server]


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
    parser.add_argument('-b', dest='batadv_iface',
                        default='bat0', metavar='<iface>',
                        help='batman-adv interface (default: bat0)')
    args = parser.parse_args()

    socketserver.ThreadingUDPServer.address_family = socket.AF_INET6

    env = {
        'batadv_dev': args.batadv_iface
    }

    if_threads = {}
    for iface in args.mcast_ifaces:
        if_threads[iface] = listen(
            iface, args.group, args.port, args.directory, env)

    while True:
        time.sleep(15)
        for iface, data in if_threads.items():
            ifidx, threads = data
            try:
                if socket.if_nametoindex(iface) != ifidx:
                    # interface has reappeared with a different index
                    if threads:
                        print("interface {0} disappeared, unbinding..."
                              .format(iface))
                        for thread in threads:
                            # make sure we remove all old socketservers first
                            thread.shutdown()
                            thread.server_close()
                        if_threads[iface] = ifidx, []
                    print("interface {0} reappeared, rebinding..."
                          .format(iface))
                    if_threads[iface] = listen(
                        iface, args.group, args.port, args.directory, env)
            except OSError as ex:
                # interface is missing, stop related server threads
                if threads:
                    print("interface {0} disappeared, unbinding..."
                          .format(iface))
                    for thread in threads:
                        thread.shutdown()
                        thread.server_close()
                    if_threads[iface] = ifidx, []


