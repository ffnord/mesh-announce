import providers


class Source(providers.DataSource):
    def call(self, vpn_protos):
        if 'wireguard' in vpn_protos:
            return open('/sys/module/wireguard/version').read().strip()

    def required_args(self):
        return ['vpn_protos']
