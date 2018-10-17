import providers
from providers.babel import dump as babeldump

class Source(providers.DataSource):
    def required_args(self):
        return ['babel_addr']

    def call(self, babel_addr):
        if babel_addr is None:
            return None
        ret = {}
        result = babeldump(babel_addr)
        for entry in result:
            if entry["add"] == "interface" and entry["up"] == "true" and entry["ipv6"] is not None:
                ret[entry["interface"]] = {
                    "ll-addr": entry["ipv6"],
                    "protocol": "babel",
                    "neighbours": ( lambda result, ifname: {
                        entry["address"]: {
                            "rxcost": int(entry["rxcost"]),
                            "txcost": int(entry["txcost"]),
                            "cost": int(entry["cost"]),
                            "reachability": int(entry["reach"],16)
                        }
                        for entry in result
                        if entry["add"] == "neighbour" and entry["if"] == ifname
                    })(result, entry["interface"])
                }
        return ret
