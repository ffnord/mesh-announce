#!/usr/bin/env python3

import metasocketserver
import socketserver
import argparse
import socket
import struct
import json
import os
from zlib import compress

from config import Config
from domain import BatadvDomain, DomainRegistry
from providers import get_providers
import util

def get_handler(providers):
    class ResponddUDPHandler(socketserver.BaseRequestHandler):
        def multi_request(self, providernames, local_env):
            ret = {}
            for name in providernames:
                try:
                    provider = providers[name]
                    ret[provider.name] = provider.call(local_env)
                except:
                    pass
            return compress(str.encode(json.dumps(ret)))[2:-4]

        def handle(self):
            data = self.request[0].decode('UTF-8').strip()
            socket = self.request[1]
            ifindex = self.request[2]
            response = None

            iface = util.ifindex_to_iface(ifindex)

            domain = DomainRegistry.get_instance().get_domain_by_interface(iface)
            if not domain:
                return

            provider_env = domain.get_provider_args()

            if data.startswith("GET "):
                response = self.multi_request(data.split(" ")[1:], provider_env)
            else:
                answer = providers[data].call(provider_env)
                if answer:
                    response = str.encode(json.dumps(answer))

            if response:
                socket.sendto(response, self.client_address)

    return ResponddUDPHandler

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="""
      %(prog)s -h
      %(prog)s [-f <configfile>] [-d <dir>]""")
    parser.add_argument('-f', dest='config',
                        default='./respondd.conf', metavar='<configfile>',
                        help='config file to use')
    parser.add_argument('-d', dest='directory',
                        default='./providers', metavar='<dir>',
                        help='data provider directory (default: $PWD/providers)')

    args = parser.parse_args()

    config = Config.from_file(args.config)
    for domname in config.get_domain_names():
        domcfg = config.get_domain_config(domname)
        DomainRegistry.get_instance().add_domain(domcfg.domain_type(domcfg))
    DomainRegistry.get_instance().set_default_domain

    metasocketserver.MetadataUDPServer.address_family = socket.AF_INET6
    metasocketserver.MetadataUDPServer.allow_reuse_address = True
    server = metasocketserver.MetadataUDPServer(
        ("", config.get_port()),
        get_handler(get_providers(args.directory))
    )
    server.daemon_threads = True

    def join_group(mcast_group, if_index=0):
        group_bin = socket.inet_pton(socket.AF_INET6, mcast_group)
        mreq = group_bin + struct.pack('@I', if_index)
        server.socket.setsockopt(
            socket.IPPROTO_IPV6,
            socket.IPV6_JOIN_GROUP,
            mreq
        )

    for (if_index, if_name) in socket.if_nameindex():
        # Check if daemon should listen on interface
        if if_name in DomainRegistry.get_instance().get_interfaces():
            dom = DomainRegistry.get_instance().get_domain_by_interface(if_name)
            # Join all multicast groups specified for this interface
            join_group(dom.get_multicast_address_link(), if_index)
            join_group(dom.get_multicast_address_site(), if_index)

    server.serve_forever()
