#!/usr/bin/env python3

import metasocketserver
import socketserver
import argparse
import socket
import struct
import json
import os
from zlib import compress

from providers import get_providers
import util

def get_handler(providers, batadv_ifaces, batadv_mesh_ipv4_overrides, env):
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

            # Find batman interface the query belongs to
            batadv_dev = util.ifindex_to_batiface(ifindex, batadv_ifaces)
            if batadv_dev == None:
                return

            # Clone global environment and populate with interface-specific data
            local_env = dict(env)
            local_env['batadv_dev'] = batadv_dev
            if batadv_dev in batadv_mesh_ipv4_overrides:
                local_env['mesh_ipv4'] = batadv_mesh_ipv4_overrides[batadv_dev]

            if data.startswith("GET "):
                response = self.multi_request(data.split(" ")[1:], local_env)
            else:
                answer = providers[data].call(local_env)
                if answer:
                    response = str.encode(json.dumps(answer))

            if response:
                socket.sendto(response, self.client_address)

    return ResponddUDPHandler

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="""
      %(prog)s -h
      %(prog)s [-p <port>] [-g <group>] [-i [<group>%%]<if0>] [-i [<group>%%]<if1> ..] [-d <dir>] [-b <batman_iface>[:<mesh_ipv4>] [-n <domain code>] [-c <domain_code_file>] ..]""")
    parser.add_argument('-p', dest='port',
                        default=1001, type=int, metavar='<port>',
                        help='port number to listen on (default 1001)')
    parser.add_argument('-g', dest='link_group',
                        default='ff02::2:1001', metavar='<link local group>',
                        help='link-local multicast group (default ff02::2:1001), set to emtpy string to disable')
    parser.add_argument('-s', dest='site_group',
                        default='ff05::2:1001', metavar='<site local group>',
                        help='site-local multicast group (default ff05::2:1001), set to empty string to disable')
    parser.add_argument('-i', dest='mcast_ifaces',
                        action='append', default=[ 'bat0' ], metavar='<iface>',
                        help='listening interface (default bat0), may be specified multiple times')
    parser.add_argument('-d', dest='directory',
                        default='./providers', metavar='<dir>',
                        help='data provider directory (default: $PWD/providers)')
    parser.add_argument('-b', dest='batadv_ifaces',
                        action='append', default=[ 'bat0' ], metavar='<iface>',
                        help='batman-adv interface to answer for (default: bat0). Specify once per domain')
    parser.add_argument('-m', dest='mesh_ipv4',
                        metavar='<mesh_ipv4>',
                        help='mesh ipv4 address')
    parser.add_argument('-n', dest='domain_code', metavar='<domain code>',
                        help='(default) domain code for system/domain_code')
    parser.add_argument('-c', dest='domain_code_file', metavar='<domain code_file>',
                        help='domain_code.json path (if info is not in file, fallback to -n\'s value)')

    args = parser.parse_args()

    # Read domain-codes from file
    known_codes = util.read_domainfile(args.domain_code_file)

    # Extract batman interfaces from commandline parameters
    # and overwrite domain-codes from file with commandline arguments
    batadv_mesh_ipv4_overrides = { }
    batadv_ifaces = [ ]
    for ifspec in args.batadv_ifaces:
        iface, *left_over = ifspec.split(':')
        batadv_ifaces.append(iface)
        try:
            # if left_over list is not empty, there is at least an override address
            possible_override = left_over.pop(0)
            # this clause is necessary in case one does not specify an ipv4 override, but a domain-code
            if '' != possible_override:
                batadv_mesh_ipv4_overrides[iface] = possible_override
            # if left_over list is not empty, there is a domain_code
            known_codes[iface] = left_over.pop(0)
        except IndexError:
            continue

    global_handler_env = { 'domain_code': args.domain_code, 'known_codes': known_codes, 'mesh_ipv4': args.mesh_ipv4 }

    metasocketserver.MetadataUDPServer.address_family = socket.AF_INET6
    metasocketserver.MetadataUDPServer.allow_reuse_address = True
    server = metasocketserver.MetadataUDPServer(
        ("", args.port),
        get_handler(get_providers(args.directory), batadv_ifaces, batadv_mesh_ipv4_overrides, global_handler_env)
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

    # Extract multicast interfaces from commandline parameters
    mcast_iface_groups = { }
    for ifspec in args.mcast_ifaces:
        iface, *groups = reversed(ifspec.split('%'))
        # Populate with default link and site mcast groups if entry not yet created
        if not iface in mcast_iface_groups:
            mcast_iface_groups[iface] = [ group for group in [ args.link_group, args.site_group ] if len(group) > 0 ]
        # Append group specified on commndline
        mcast_iface_groups[iface] += groups

    for (if_index, if_name) in socket.if_nameindex():
        # Check if daemon should listen on interface
        if if_name in mcast_iface_groups:
            groups = mcast_iface_groups[if_name]
            # Join all multicast groups specified for this interface
            for group in groups:
                join_group(group, if_index)

    server.serve_forever()
