Gluon Status Scripts for Servers
--------------------------------

These scripts are replacements for the *[respondd]* and *[gluon-alfred]* packages in Gluon that can be used on servers (like gateways) to broadcast the information needed to for example display the name of the server on node maps.

[respondd]: https://github.com/freifunk-gluon/packages/tree/master/net/respondd
[gluon-alfred]: https://github.com/freifunk-gluon/gluon/tree/master/package/gluon-alfred

## Dependencies

 * lsb\_release
 * ethtool
 * python3 (>= 3.3)
 * python3-netifaces
 * If using alfred: alfred binary in PATH

## Setup

### Alfred

Add _announce.sh_ to your cronjobs, and let it run every minute, e.g.
```
PATH=/opt/alfred/:/bin:/usr/bin:/sbin:$PATH /opt/mesh-announce/announce.sh
```

### Respondd

Assuming you are using systemd, copy the `respondd.service` file to `/etc/systemd/system/`, and adapt the path to your checkout of the repository in the line starting with `ExecStart=`.

Afterwards, execute these commands:
```
systemctl daemon-reload
systemctl start respondd
# autostart on boot
systemctl enable respondd
```
