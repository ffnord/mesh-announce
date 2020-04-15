Gluon Status Scripts for Servers
--------------------------------

These scripts are replacements for the *[respondd]* and *[gluon-alfred]*
packages in Gluon that can be used on servers (like gateways) to broadcast the
information needed for example to display the name of the server on node-maps.

[respondd]: https://github.com/freifunk-gluon/packages/tree/master/net/respondd
[gluon-alfred]: https://github.com/freifunk-gluon/gluon/tree/master/package/gluon-alfred

## Dependencies

 * lsb\_release
 * ethtool
 * python3 (>= 3.3)
 * If using alfred: alfred binary in PATH

## Setup

    git clone https://github.com/ffnord/mesh-announce /opt/mesh-announce
    cp /opt/mesh-announce/respondd.service /etc/systemd/system/
    # adapt the line ExecStart in /etc/systemd/system/respondd.service (see "commandline options")
    systemctl daemon-reload
    systemctl start respondd
    systemctl status respondd

## Upgrade

    cp /opt/mesh-announce/respondd.service /etc/systemd/system/
    git pull
    # check /etc/systemd/system/respondd.service for new options/adaptions
    systemctl daemon-reload
    systemctl restart respondd
    systemctl status respondd

Note that you might need to transition from the old, commandline argument based config method to
the new config file based method when upgrading from an older version

### Alfred

Open the Alfred port UDP 16962 in your firewall. Add _announce.sh_ to your
cronjobs, and let it run every minute, e.g.

    PATH=/opt/alfred/:/bin:/usr/bin:/sbin:$PATH /opt/mesh-announce/announce.sh

### Respondd

Assuming you are using systemd, copy the `respondd.service` file to
`/etc/systemd/system/`. Open the copy and adapt the path to your checkout of
the repository and the interface names in the line starting with `ExecStart=`.
Afterwards, start the service and optionally set it to autostart:

    systemctl daemon-reload
    systemctl start respondd
    # autostart on boot
    systemctl enable respondd

Furthermore, you have to open UDP port 1001 in your IPv6 firewall for all mesh
and B.A.T.M.A.N. advanced interfaces. Please *don't* open the port globally, as
it can be used for traffic amplification attacks. You also might want to
ratelimit it on the allowed interfaces for the same reason.

#### Commandline options

Those are all available options (`respondd --help`):

```
usage: 
      respondd.py -h
      respondd.py [-f <configfile>] [-d <dir>]

optional arguments:
  -h, --help       show this help message and exit
  -f <configfile>  config file to use (default: $PWD/respondd.conf)
  -d <dir>         data provider directory (default: $PWD/providers)

```

#### Configuration

Configuration is done via a ini-style config file. A possible config for a setup with a single batman domain in outlined in `respondd.conf.example`.
The following is a more complete breakdown of the settings required:
```
# Default settings
[Defaults]
# Listen port, defaults to 1001
Port: 1001
# Default multicast listen addresses
MulticastLinkAddress: ff02::2:1001
MulticastSiteAddress: ff05::2:1001
# Default domain to use
DefaultDomain: <domain code>
# Default domain type
DomainType: batadv

# A domain
[<domain code>]
# Batman interface, mandatory
BatmanInterface: <your-batman-if>
# Other listen interfaces
Interfaces: <your-clientbridge-if>, <your-mesh-vpn-if>
# IPv4 gateway option for ddhcpd
IPv4Gateway: <mesh ipv4 address>
```

 * `<your-clientbridge-if>`: interfacename of mesh-bridge (for example br-ffXX)
 * `<your-mesh-vpn-if>`: interfacename of fastd or tuneldigger (for example ffXX-mvpn)
 * `<your-batman-if>`: B.A.T.M.A.N interfacename (usually bat-ffXX)
 * `<mesh ipv4 address>`: The ipv4 address of this gateway (usually the ip on interface `<your-clientbridge-if>`)  
    you can get the ip with `ip a s dev br-ffXX|grep inet|head -n1|cut -d" " -f 6|sed 's|/.*||g'`
 * `<domain code>`: The internal domain_code, identical with the gluon domain_name

The <mesh ipv4 address> can be requested for example by
[ddhcpd](https://github.com/TobleMiner/gluon-sargon/blob/feature-respondd-gateway-update/ddhcpd/files/usr/sbin/ddhcpd-gateway-update#L3)
via

    `gluon-neighbour-info -p 1001 -d ff02::1 -i bat0 -r gateway`
    
This will request all json objects for all gateways. The json object for the
gateway can then be selected by the known macadress. The IPv4 address is stored in
`node_id.address.ipv4`.

Configuration for a multi-domain site (domains 'one', 'two' and 'three') might look like this:

```
# Default settings
[Defaults]
# Listen port, defaults to 1001
Port: 1001
# Default multicast listen addresses
MulticastLinkAddress: ff02::2:1001
MulticastSiteAddress: ff05::2:1001
# Default domain type
DomainType: batadv
# IPv4 gateway option for ddhcpd
IPv4Gateway: 10.42.0.1

# First domain
[one]
# Batman interface, mandatory for batman domains
BatmanInterface: bat-one
# Other listen interfaces
Interfaces: br-one, mvpn-one

# Second domain
[two]
# Batman interface, mandatory for batman domains
BatmanInterface: bat-two
# Other listen interfaces
Interfaces: br-two, mvpn-two

# Third domain
[three]
# Batman interface, mandatory for datman domains
BatmanInterface: bat-three
# Other listen interfaces
Interfaces: br-three, mvpn-three
```

In a more complex configuration involving the distributed DHCP deamon ddhcpd you might want to advertise different ipv4 gateways depending on the domain the query came from.
This can be realized by adding gateway address overrides to the corresponding batman interfaces:

```
# Default settings
[Defaults]
# Listen port, defaults to 1001
Port: 1001
# Default multicast listen addresses
MulticastLinkAddress: ff02::2:1001
MulticastSiteAddress: ff05::2:1001
# Default domain type
DomainType: batadv

# First domain
[one]
# Batman interface, mandatory for batman domains
BatmanInterface: bat-one
# Other listen interfaces
Interfaces: br-one, mvpn-one
# IPv4 gateway option for ddhcpd
IPv4Gateway: 10.42.0.1

# Second domain
[two]
# Batman interface, mandatory for batman domains
BatmanInterface: bat-two
# Other listen interfaces
Interfaces: br-two, mvpn-two
# IPv4 gateway option for ddhcpd
IPv4Gateway: 10.42.8.1

# Third domain
[three]
# Batman interface, mandatory for datman domains
BatmanInterface: bat-three
# Other listen interfaces
Interfaces: br-three, mvpn-three
# IPv4 gateway option for ddhcpd
IPv4Gateway: 10.42.16.1
```

### Debugging

When something goes wrong, the first step should be to look at the error log:

    sudo journalctl -u respondd.service
