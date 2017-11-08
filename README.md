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

Assuming you are using systemd:
```
cp respondd.service /etc/systemd/system/
```
- adapt the interfaces in the line starting with `ExecStart=` (If you have a custom path, adapt the path to your checkout of the repository)
- open UDP port 1001 in your firewall:
```
iptables -A bat-input -p udp -m udp --dport 1001 -m comment --comment respondd -j ACCEPT
iptables -A mesh-input -p udp -m udp --dport 1001 -m comment --comment respondd -j ACCEPT
ip6tables -A bat-input -p udp -m udp --dport 1001 -m comment --comment respondd -j ACCEPT
ip6tables -A mesh-input -p udp -m udp --dport 1001 -m comment --comment respondd -j ACCEPT
```

Afterwards, execute these commands:
```
systemctl daemon-reload
systemctl start respondd
# autostart on boot
systemctl enable respondd
```
