import providers


class Source(providers.DataSource):
    def call(self, vpn_protos, fastd_pubkey):
        if 'fastd' in vpn_protos:
            return fastd_pubkey

    def required_args(self):
        return ['vpn_protos', 'fastd_pubkey']
