import providers


class Source(providers.DataSource):
    def call(self, vpn_protos, wireguard_pubkey):
        if 'wireguard' in vpn_protos:
            return wireguard_pubkey

    def required_args(self):
        return ['vpn_protos', 'wireguard_pubkey']
