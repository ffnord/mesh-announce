import providers


class Source(providers.DataSource):
    def call(self, vpn_protos, vpn_pubkey):
        if 'fastd' in vpn_protos:
            return vpn_pubkey

    def required_args(self):
        return ['vpn_protos', 'vpn_pubkey']
