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

#### commandline options

Those are all available options (`respondd --help`):

```
      respondd.py -h
      respondd.py [-p <port>] [-g <group>] [-i [<group>%]<if0>] [-i [<group>%]<if1> ..] [-d <dir>] [-b <batman_iface>[:<mesh_ipv4>] ..]

optional arguments:
  -h, --help            show this help message and exit
  -p <port>             port number to listen on (default 1001)
  -g <link local group>
                        link-local multicast group (default ff02::2:1001), set
                        to emtpy string to disable
  -s <site local group>
                        site-local multicast group (default ff05::2:1001), set
                        to empty string to disable
  -i <iface>            listening interface (default bat0), may be specified
                        multiple times
  -d <dir>              data provider directory (default: $PWD/providers)
  -b <iface>            batman-adv interface to answer for (default: bat0).
                        Specify once per domain
  -m <mesh_ipv4>        mesh ipv4 address
  -n <domain_code>      Gateway domain_code for nodeinfo/system/domain_code
```

This is a possible configuration for a site with a single domain:

    `respondd.py -d /opt/mesh-announce/providers -i <your-clientbridge-if> -i <your-mesh-vpn-if> -b <your-batman-if> -m <mesh ipv4 address>`

 * `<your-clientbridge-if>`: interfacename of mesh-bridge (for example br-ffXX)
 * `<your-mesh-vpn-if>`: interfacename of fastd or tuneldigger (for example ffXX-mvpn)
 * `<your-batman-if>`: B.A.T.M.A.N interfacename (usually bat-ffXX)
 * `<mesh ipv4 address>`: The ipv4 address of this gateway (usually the ip on interface `<your-clientbridge-if>`)  
    you can get the ip with `ip a s dev br-ffXX|grep inet|head -n1|cut -d" " -f 6|sed 's|/.*||g'`
 * `<domain_code>`: The internal domain_code, identical with the gluon domain_name

The ipv4 address can be requested for example by
[ddhcpd](https://github.com/TobleMiner/gluon-sargon/blob/feature-respondd-gateway-update/ddhcpd/files/usr/sbin/ddhcpd-gateway-update#L3)
via

    `gluon-neighbour-info -p 1001 -d ff02::1 -i bat0 -r gateway`
    
This will request all json objects for all gateways. The json object for the
gateway can then be selected by the known macadress. The ip4 is stored in
`node_id.address.ipv4`.

Configuration for a multi-domain site (domains 'one', 'two' and 'three') might look like this:

    `respondd.py -d /opt/mesh-announce/providers -i meshvpn-one -i br-one -i bat-one -b bat-one -i meshvpn-two -i br-two -i bat-two -b bat-two -i meshvpn-three -i br-three -i bat-three -b bat-three`

In a more complex configuration involving the distributed DHCP deamon ddhcpd you might want to advertise different ipv4 gateways depending on the domain the query came from.
This can be realized by adding gateway address overrides to the corresponding batman interfaces:

    `respondd.py -d /opt/mesh-announce/providers -i meshvpn-one -i br-one -i bat-one -b bat-one:10.42.1.1 -i meshvpn-two -i br-two -i bat-two -b bat-two:10.42.2.1 -i meshvpn-three -i br-three -i bat-three -b bat-three:10.42.3.1`


### Debugging

When something goes wrong, the first step should be to look at the error log:

    sudo journalctl -u respondd.service
