import providers
from os.path import exists


class Source(providers.DataSource):
    def call(self, vpn_protos):
        if 'wireguard' in vpn_protos:
            return exists("/sys/module/wireguard/initstate")

    def required_args(self):
        return ['vpn_protos:wireguard']
