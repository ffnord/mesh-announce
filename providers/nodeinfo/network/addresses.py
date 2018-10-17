import providers
from ipaddress import IPv6Address
from glob import glob
from providers.babel import dump as babeldump

class Source(providers.DataSource):
    def required_args(self):
        return ['batadv_dev', 'babel_addr']

    def call(self, batadv_dev, babel_addr):
        # filter addresses from /proc/net/if_inet6 belonging to given ifaces
        ret = (lambda ifaces:
            [
                str(IPv6Address(int(line[0], 16)))
                for line in map(str.split, open('/proc/net/if_inet6'))
                if line[5] in ifaces
                    and not int(line[4], 16) & (0x40 | 0x20)
                    # address is neither tentative nor deprecated
            ]
        )(
            # generate the list of ifaces
            [ batadv_dev ] +
            list(map(
                lambda s: s[len('/sys/class/net/{}/upper_'.format(batadv_dev)):],
                glob('/sys/class/net/{}/upper_*'.format(batadv_dev))
            ))
        )
        if babel_addr is not None:
            for entry in babeldump(babel_addr):
                if entry["add"] == "interface" and entry["up"] == "true":
                    ret.append(entry["ipv6"])

        return ret
