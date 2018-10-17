import providers
from providers.util import call
from providers.babel import dump as babeldump

class Source(providers.DataSource):
    def required_args(self):
        return ['batadv_dev', 'babel_addr']

    def call(self, batadv_dev, babel_addr):
        if babel_addr is None and batadv_dev is None :
            return None
        ret = {}
        if babel_addr is not None:
            ret["babel"] = {
                "interfaces": {
                    "tunnel": (lambda result: [
                        entry["ipv6"]
                        for entry in result
                        if entry["add"] == "interface" and entry["up"] == "true"
                    ])(babeldump(babel_addr))
                }
            }
        if batadv_dev is not None:
            ret[batadv_dev] = {
                "interfaces": {
                    "tunnel": [
                        open('/sys/class/net/{}/address'.format(iface)).read().strip()
                        for iface in map(
                            lambda line: line.split(':')[0],
                            call(['batctl', '-m', batadv_dev, 'if'])
                        )
                    ]
                }
            }
        return ret
