Gluon Status Scripts for Servers
--------------------------------

These scripts are replacements for the *[respondd]* and *[gluon-alfred]* packages in Gluon that can be used on servers (like gateways) to broadcast the information needed to for example display the name of the server on node maps.

[respondd]: https://github.com/freifunk-gluon/packages/tree/master/net/respondd
[gluon-alfred]: https://github.com/freifunk-gluon/gluon/tree/master/package/gluon-alfred

## Dependencies

 * lsb\_release
 * ethtool
 * python3 (>= 3.3)
 * If using alfred: alfred binary in PATH

## Setup
```
git clone https://github.com/ffnord/mesh-announce /opt/mesh-announce
```

### Alfred

Open the Alfred port UDP 16962 in your firewall. Add _announce.sh_ to your cronjobs, and let it run every minute, e.g.
```
PATH=/opt/alfred/:/bin:/usr/bin:/sbin:$PATH /opt/mesh-announce/announce.sh
```

### Respondd

Assuming you are using systemd, copy the `respondd.service` file to `/etc/systemd/system/`. Open the copy and adapt the path to your checkout of the repository and the interface names in the line starting with `ExecStart=`. Afterwards, start the service and optionally set it to autostart:
```
systemctl daemon-reload
systemctl start respondd
# autostart on boot
systemctl enable respondd
```

Furthermore, you have to open UDP port 1001 in your IPv6 firewall for all mesh and B.A.T.M.A.N. advanced interfaces. Please *don't* open the port globally, as it can be used for traffic amplification attacks. You also might want to ratelimit it on the allowed interfaces for the same reason.
