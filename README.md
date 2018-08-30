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

    respondd.py [-p <port>] [-g <group> -i <if0> [-i <if1> ..]] [-d <dir>]

for example:

    respondd.py -d /opt/mesh-announce/providers -i <your-clientbridge-if> -i <your-mesh-vpn-if> -b <your-batman-if> -m <mesh ipv4 address>

 * `<your-clientbridge-if>`: interfacename of mesh-bridge (for example br-ffXX)
 * `<your-mesh-vpn-if>`: interfacename of fastd or tuneldigger (for example ffXX-mvpn)
 * `<your-batman-if>`: B.A.T.M.A.N interfacename (usually bat-ffXX)
 * `<mesh ipv4 address>`: The ipv4 address of this gateway (usually the ip on interface `<your-clientbridge-if>`)  
    you can get the ip with `ip a s dev br-ffXX|grep inet|head -n1|cut -d" " -f 6|sed 's|/.*||g'`
    
The ipv4 address can be requested for example by
[ddhcpd](https://github.com/TobleMiner/gluon-sargon/blob/feature-respondd-gateway-update/ddhcpd/files/usr/sbin/ddhcpd-gateway-update#L3)
via

    gluon-neighbour-info -p 1001 -d ff02::1 -i bat0 -r gateway
    
This will request all json objects for all gateways. The json object for the
gateway can then be selected by the known macadress. The ip4 is stored in
`node_id.address.ipv4`.

### Debugging

When something goes wrong, the first step should be to look at the error log:

    sudo journalctl -u respondd.service
